import json

from sage.all import *

from distributed.base import BASE_URL
from distributed.helpers.worker_handling import create_radix_system
from distributed.optimizing import phi_optimize_target_function
from distributed.server_connection import call_server, ServerJsonEncoder
from gns import complex_target_function, Timer

cand_num = 10
num_of_cand_to_mutate = 10
mutate_num = 100
iterate_num = 500

def optimizing(data, ns):
    optimizedNs, transformation = ns.optimize(candNum=cand_num,
                                              numOfCandToMutate=num_of_cand_to_mutate,
                                              mutateNum=mutate_num,
                                              iterateNum=iterate_num,
                                              targetFunction=complex_target_function,
                                              debug=False,
                                              returnTransformationAlso=true,
                                              timeout=1800)

    isOptimized = transformation != matrix.identity(ns.getDimension())

    if isOptimized:
        res = call_server(BASE_URL + "add-similar",
                          {},
                          {
                              'RSFromId': data["id"],
                              'token': 'asdasd',
                              'transformMatrix': json.dumps(transformation, cls=ServerJsonEncoder),
                              'transformType': 'optimizer:complex',
                              'transformProperties': json.dumps({
                                  "candNum": cand_num,
                                  "numOfCandToMutate": num_of_cand_to_mutate,
                                  "mutateNum": mutate_num,
                                  "iterateNum": iterate_num
                              }, cls=ServerJsonEncoder),
                              'base': json.dumps(optimizedNs.get_base(), cls=ServerJsonEncoder),
                              'digits': json.dumps(optimizedNs.get_digits(), cls=ServerJsonEncoder),
                              'digitsGeneratedBy': data['digitsGeneratedBy'],
                              'baseGeneratedBy': data['baseGeneratedBy'],
                              'priority': max(data["priority"] - 10, 0),
                          }
                          )

        call_server(BASE_URL + "add-properties",
                    {},
                    {
                        'RSId': res["id"],
                        'properties': json.dumps({
                            'optimizedFromWith': 'complex'
                        }, cls=ServerJsonEncoder),
                        'token': 'asdasd',
                    }
                    )

    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'optimized': 1 if isOptimized else 0
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )


def measureTime(data, ns):

    pointLimit = 10000

    bestsRaw = call_server(BASE_URL + "find-best-optimalizations",
                           {
                               'RSId': data["id"],
                               'token': 'asdasd',
                           }
                           )
    bests = bestsRaw["data"]

    optimalizations = {}
    for optimalizationType in bests:
        act = bests[optimalizationType]
        ns = create_radix_system(act["system"])
        resultTransform = matrix.identity(ns.get_dimension())
        for transform in act["transform_matrices"]:
            resultTransform = resultTransform * Matrix(ZZ, transform)
        optimalizations[optimalizationType] = {
            "system": ns,
            "transform": resultTransform
        }

    properties = {"measureTimeDone": "1"}

    t = Timer()

    for optName in optimalizations:
        opt = optimalizations[optName]

        t.start_timer()
        properties[optName + ":IsGNSResult"] = 1 if opt["system"].decideGNS(pointLimit=pointLimit) else 0
        properties[optName + ":IsGNSTime"] = t.get_time()

        # Step from the original version
        optimizedPhi, optimizePhiT = ns.optimize(cand_num, num_of_cand_to_mutate, mutate_num, iterate_num,
                                                 lambda actVal, T: phi_optimize_target_function(actVal, T, opt[
                                                     "transform"].inverse()), return_transformation_also=true,
                                                 debug=False, timeout=None)

        transformMatrix = optimizePhiT * opt["transform"].inverse()
        t.start_timer()
        properties[optName + ":twoTransform:IsGNSResult"] = 1 if optimizedPhi.decideGNS(pointLimit=pointLimit,
                                                                                        startPointSource=opt[
                                                                                            "system"],
                                                                                        pointTransform=transformMatrix) else 0
        properties[optName + ":twoTransform:IsGNSTime"] = t.get_time()

        # Step from the optimized version
        optimizedPhi, optimizePhiT = opt["system"].optimize(cand_num, num_of_cand_to_mutate, mutate_num, iterate_num,
                                                            phi_optimize_target_function,
                                                            return_transformation_also=True, debug=False,
                                                            timeout=None)
        t.start_timer()
        properties[optName + ":twoTransform2:IsGNSResult"] = 1 if optimizedPhi.decideGNS(pointLimit=pointLimit,
                                                                                         startPointSource=opt[
                                                                                             "system"],
                                                                                         pointTransform=optimizePhiT) else 0
        properties[optName + ":twoTransform2:IsGNSTime"] = t.get_time()

    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps(properties, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )
