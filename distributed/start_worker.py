import datetime
import socket

from distributed.base import BASE_URL
from gns import complex_target_function, dimension_target_function, calculate_volume, Timer, Drawer
from orbit_count import count_orbits
from sage.all import *
from gns.SemiRadixSystem import SemiRadixSystem
from gns.digits import ShiftedCanonicalDigits, CanonicalDigits, SymmetricDigits, Digits
from gns.Operator import AlwaysExceptionOperator
from server_connection import call_server, ServerJsonEncoder
from optimizing import phi_optimize_target_function, coef_string_to_polynom, create_companion_matrix_from_polynom


def get_actual_date_time_string():
    return '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())


cand_num = 10
num_of_cand_to_mutate = 10
mutate_num = 100
iterate_num = 500


def create_radix_system(data):
    digits = []
    if data['digits'] == "canonical":
        digits = CanonicalDigits()
    elif data['digits'] == "symmetric":
        digits = SymmetricDigits()
    else:
        digits = Digits(data['digits'])

    m = Matrix(ZZ, data['base'])
    ns = SemiRadixSystem(m, digits, AlwaysExceptionOperator())
    return ns

def run_work(callback, url=BASE_URL + "list", data: dict=None):
    if data is None:
        data = {}
    radix_systems = call_server(url, data)
    progressed = []
    for data in radix_systems:
        if len(data['base']) < 2:
            continue

        ns = create_radix_system(data)
        print("Progress:", data["id"], len(data['base']), get_actual_date_time_string())
        callback(data, ns)
        progressed.append(data)
    return progressed

import time

def build_request_data(lockName : str = None, extraData=None):
    if extraData is None:
        extraData = {}
    query_data = {
        ".block": "null",
        "propertyValue": "in progress by " + socket.gethostname(),
        "sort_property": "volume",
        "sort_direction": "asc"
    }
    if lockName is not None:
        query_data.update({
            "." + lockName: "null",
            "propertyName": lockName
            })

    query_data.update(extraData)
    return query_data

def start_processor(callback, lock_name, conditions=None, input_run_work=run_work):
    if conditions is None:
        conditions = {}
    baseTimeout = 2
    maxTimout = 60
    tryCounter = 0
    while True:
        processed = None
        while processed == None or len(processed) > 0:
            print("PROCESSSS", get_actual_date_time_string())
            queryData = build_request_data(lock_name, conditions)
            processed = input_run_work(callback, BASE_URL + "set-property-for-first", queryData)
            for processedRs in processed:
                call_server(BASE_URL + "remove-property", {}, {"id": processedRs["id"], "propertyName": lock_name})

            if len(processed):
                tryCounter = 0

        tryCounter += 1

        actualWait = min(maxTimout, pow(baseTimeout, tryCounter))
        print("No job! Waiting " + str(actualWait) + " sec.", get_actual_date_time_string())
        time.sleep(actualWait)

def test(data, ns):
    print(ns)

def generate_multiplications(data, ns):
    radix_systems = call_server(BASE_URL + "list", {".dimension": ns.getDimension()})
    for data2 in radix_systems:
        print("====================")
        if len(data2['base']) < 2:
            continue
        ns2 = create_radix_system(data2)
        multi_base = ns.get_base() * ns2.get_base()
        print(ns.get_base())
        print(ns2.get_base())
        digits1 = ns.get_digits()
        digits2 = ns2.get_digits()
        print("--A")
        print(ns.get_base())
        print("--")
        print(digits1)
        print("--")
        print("--B")
        print(ns2.get_base())
        print("--")
        print(digits2)
        print("--")
        new_digits = [vector(digits1[d1It]) + ns.get_base() * vector(digits2[d2It]) for d1It in range(len(digits1))
                     for d2It in range(len(digits2))]
        print(new_digits)
        print(multi_base)
        try:
            ns3 = SemiRadixSystem(multi_base, new_digits, AlwaysExceptionOperator())
            generatedBy = str(data["id"]) + "," + str(data2["id"])
            # upload_rs(ns3,"multiplication2",generatedBy,generatedBy,generatedBy)
        except Exception as e:
            print(e)

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

def coverToDistances(cover):
    return [abs(cover[0][i] - cover[1][i]) for i in range(len(cover[0]))]

def dimensionOptimize(data, ns):
    print(ns.getCoverBox())
    print(coverToDistances(ns.getCoverBox()))
    optimizedNs, transformation = ns.optimize(candNum=cand_num, numOfCandToMutate=num_of_cand_to_mutate,
                                              mutateNum=mutate_num, iterateNum=iterate_num,
                                              targetFunction=dimension_target_function, debug=True,
                                              returnTransformationAlso=true, timeout=1800)
    print(coverToDistances(ns.getCoverBox()))

def optimizingVolume(data, ns):
    optimizedNs, transformation = ns.optimize(candNum=cand_num, numOfCandToMutate=num_of_cand_to_mutate,
                                              mutateNum=mutate_num, iterateNum=iterate_num,
                                              targetFunction=calculate_volume, debug=False,
                                              returnTransformationAlso=true, timeout=1800)

    isOptimized = transformation != matrix.identity(ns.getDimension())

    if isOptimized:
        res = call_server(BASE_URL + "add-similar",
                          {},
                          {
                              'RSFromId': data["id"],
                              'token': 'asdasd',
                              'transformMatrix': json.dumps(transformation, cls=ServerJsonEncoder),
                              'transformType': 'optimizer:volume',
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
                            'optimizedFromWith': 'volume'
                        }, cls=ServerJsonEncoder),
                        'token': 'asdasd',
                    }
                    )

    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'volumeOptimized': 1 if isOptimized else 0
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )

def calculateVolumeCallback(data, ns):
    volume = ns.getCoverBoxVolume()
    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'volume': volume
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )

def calculateDimension(data, ns):
    dim = ns.getDimension()
    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'dimension': dim
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )

def decide(data, ns):
    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'gns': 1 if ns.isGNS() else 0
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

def recursiveNumericalApprox(obj):
    if type(obj) in [type([]), type((1, 2, 3))]:
        return [recursiveNumericalApprox(x) for x in obj]
    else:
        numerical_approx = getattr(obj, "numerical_approx", None)
        if callable(numerical_approx):
            return obj.numerical_approx()
        else:
            return obj

def calculateEigenvalues(data, ns):
    eigenvals = ns.get_base().eigenvalues()
    print(eigenvals)
    #        print([method_name for method_name in dir(eigenvals[0]) if callable(getattr(eigenvals[0], method_name))])
    eigenvals = [x.numerical_approx() for x in eigenvals]
    eigenvals.sort()
    eigenvectors = ns.get_base().eigenvectors_right()
    eigenvectors = recursiveNumericalApprox(eigenvectors)
    eigenvalueNorms = [abs(x) for x in eigenvals]
    eigenvalueNorms.sort()
    print(type(eigenvals[0]))
    print(str(eigenvals[0]), abs(eigenvals[0]))
    print(str(eigenvals[-1]), abs(eigenvals[-1]))
    print("Vectors")
    print(str(eigenvectors))
    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'eigenvalues': str(eigenvals),
                        'eigenvectors': str(eigenvectors),
                        'eigenvalueNorms': str(eigenvalueNorms),
                        'eigenvalueMin': str(eigenvals[0]),
                        'eigenvalueMax': str(eigenvals[-1]),
                        'eigenvalueNormMin': str(eigenvalueNorms[0]),
                        'eigenvalueNormMax': str(eigenvalueNorms[-1]),
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )

def calculate_signature(data, ns):
    stateMatrix, signature, cycles, orbitLengths, sourceDistances = count_orbits(ns)
    if False:
        print("STATE")
        print(stateMatrix)
        print("SIGNATURE")
        print(signature)
        print("CYCLES")
        print(cycles)
        print("orbitLengths")
        print(orbitLengths)
        print("sourceDistances")
        print(sourceDistances)

    props = {
        'signature': json.dumps(signature, cls=ServerJsonEncoder),
        'periodicPointCount': len(signature),
        'gns': 1 if len(signature) == 1 else 0
    }

    for cycleIt in range(len(cycles)):
        #           if cycleIt > 0:
        props["period" + str(cycleIt)] = json.dumps(cycles[cycleIt], cls=ServerJsonEncoder)
        props["period" + str(cycleIt) + "Length"] = len(cycles[cycleIt])
        props["period" + str(cycleIt) + "orbitLengths"] = json.dumps(orbitLengths[cycleIt], cls=ServerJsonEncoder)
        props["period" + str(cycleIt) + "sourceDistances"] = json.dumps(sourceDistances[cycleIt],
                                                                        cls=ServerJsonEncoder)

    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps(props, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )

import json

'''
from sage.rings.polynomial.cyclotomic import cyclotomic_coeffs
def uploadCyclomaticCases(nArray):
    for i in nArray:
        x = polygen(QQ)
        p = cyclotomic_polynomial(i)(x+2)
        m = createCompanionMatrixFromPolynom(p)
        try:
            rs = SemiRadixSystem(m,CanonicalDigits(),AlwaysExceptionOperator());
            upload_rs(rs,"cyclomatic-2p-canonical","cyclomatic",'canonical')
            rs = SemiRadixSystem(m,SymmetricDigits(),AlwaysExceptionOperator());
            upload_rs(rs,"cyclomatic-2p-symmetric","cyclomatic",'symmetric')
        except Exception as e:
            print "'",p,"\tfailed\t",e.value
'''

def operator_test_run_worker(url=BASE_URL + "list", data=None):
    if data is None:
        data = {}
    radix_systems = call_server(url, data)
    progressed = []
    for data in radix_systems:
        if len(data['base']) < 2:
            continue

        digits = Digits(data['digits'])

        m = Matrix(ZZ, data['base'])

        call_server(BASE_URL + "add-properties",
                    {},
                    {
                        'RSId': data["id"],
                        'properties': json.dumps({
                            'block': "operator fail",
                            'operatorTest': 'ok'
                        }, cls=ServerJsonEncoder),
                        'token': 'asdasd',
                    }
                    )
        print("Test:", data["id"], len(data['base']))
        ns = SemiRadixSystem(m, digits)
        call_server(BASE_URL + "remove-property", {}, {"id": data["id"], "propertyName": "block"})
        progressed.append(data)
    return progressed

    # run_work(optimizingVolume,data={"id":486})

#    run_work(calculate_signature,data={"id":472},url="http://numsys.info/web/radix-system/list")
#    run_work(calculate_signature,data={"id":464},url="http://numsys.info/web/radix-system/list")
# run_work(calculate_signature,data={".volume":"<30"})
# upload_rs(SemiRadixSystem(Matrix(ZZ,2,[[0,-3],[1,0]]),[[0,0],[1,0],[-1,1]]),"manual","manual",'manual')
# upload_rs(SemiRadixSystem(Matrix(ZZ,2,[[2,-1],[1,2]]),[[0,0],[1,0],[0,1],[0,-1],[-6,-5]]),"manual","manual",'manual')
#    run_work(calculate_signature,data={"id":651})
#    run_work(calculate_signature,data={"id":652})
if len(sys.argv) == 1:
    print("Need a parameter: volume|signature|optimize|garsia|cyclomatic")
elif sys.argv[1] == "dimension":
    start_processor(calculateDimension, "progress_dimension", {".dimension": "null"})
elif sys.argv[1] == "volume":
    start_processor(calculateVolumeCallback, "progress_volume", {".volume": "null"})
elif sys.argv[1] == "smallvolume":
    start_processor(calculateVolumeCallback, "progress_volume", {".volume": "null", ".dimension": "<7"})
elif sys.argv[1] == "smallsignature":
    start_processor(calculate_signature, "progress_signature",
                   {".signature": "null", ".optimized": "0", ".volume": "<1000000"})
elif sys.argv[1] == "mediumsignature":
    start_processor(calculate_signature, "progress_signature",
                   {".signature": "null", ".optimized": "0", ".volume": "<1000000000"})
elif sys.argv[1] == "signature":
    start_processor(calculate_signature, "progress_signature",
                   {".signature": "null", ".optimized": "0", ".volume": "<67108864"})
elif sys.argv[1] == "decide":
    start_processor(calculate_signature, "progress_signature", {".optimized": "0", ".gns": "null"})
elif sys.argv[1] == "optimizeStart":
    start_processor(optimizing, "progress_optimizing", {"has_similar_radix_system": 0, ".optimized": "null"})
elif sys.argv[1] == "optimize":
    start_processor(optimizing, "progress_optimizing",
                   {".optimizedFromWith": "complex", "has_similar_radix_system": 0, ".optimized": "null"})
elif sys.argv[1] == "smalloptimize":
    start_processor(optimizing, "progress_optimizing",
                   {".optimizedFromWith": "complex", "has_similar_radix_system": 0, ".volume": "<1000000",
                    ".optimized": "null"})
elif sys.argv[1] == "mediumoptimize":
    start_processor(optimizing, "progress_optimizing",
                   {".optimizedFromWith": "complex", "has_similar_radix_system": 0, ".volume": "<1000000000",
                    ".optimized": "null"})
elif sys.argv[1] == "optimizeVolumeStart":
    start_processor(optimizingVolume, "progress_optimizing_volume", {"source": "manual", ".volumeOptimized": "null"})
elif sys.argv[1] == "optimizeVolume":
    start_processor(optimizingVolume, "progress_optimizing_volume",
                   {".optimizedFromWith": "volume", ".volumeOptimized": "null"})
elif sys.argv[1] == "measureTime":
    start_processor(measureTime, "progress_measureTime",
                   {"source": "manual", ".measureTimeDone": "null", ".optimized": "1", ".volumeOptimized": "1"})
elif sys.argv[1] == "eigenvalues":
    start_processor(calculateEigenvalues, "progress_eigenvalues", {".eigenvalueMin": "null"})
elif sys.argv[1] == "optimize":
    start_processor(optimizing, "progress_optimizing",
                   {".optimizedFromWith": "complex", "has_similar_radix_system": 0, ".optimized": "null"})
elif sys.argv[1] == "operatortest":
    operator_test_run_worker(data={"size": 1000, ".operatorTest": "null", "group": "multiplication2"})
elif sys.argv[1] == "oneoperatortest":
    result = operator_test_run_worker(data={"size": 1, ".operatorTest": "null", 'source': 'manual', 'group': 'det7'})
    if len(result) == 0:
        print("NOMORE")
elif sys.argv[1] == "dimensionOptimize":
    run_work(dimensionOptimize, data={".dimension": ">2"})
elif sys.argv[1] == "generateMultiplications":
    run_work(generate_multiplications, data={".dimension": "2", "group": "<>multiplication"})
elif sys.argv[1] == "test":
    start_processor(test, "test", {".optimized": "null"})
else:
    print("Unknown Command")
