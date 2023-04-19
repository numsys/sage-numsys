from sage.all import *

from distributed.optimizing import phi_optimize_target_function
from distributed.server_connection import call_server_add_property, json_dumps_prop
from gns import complex_target_function, Timer, SemiRadixSystem, calculate_volume


def assert_equal(a,b,message):
    if a != b:
        raise Exception(message)


def optimizing(data, rs: SemiRadixSystem):
    t = Timer()
    properties_to_add = {}

    print(rs.get_base())
    print(rs.get_digits())
    t.start_timer()
    # Vol
    vol_opt_rs, vol_opt_transformation = rs.optimize(target_function=calculate_volume,return_transformation_also=true,timeout=1800)
    properties_to_add['optimize:vol_opt_transformation'] = json_dumps_prop(vol_opt_transformation)


    t.measure_time('optimize:vol:optimize')
    is_gns = vol_opt_rs.decide_gns()
    t.measure_time('optimize:vol:decide')

    # Vol + Phi
    phi_opt_rs_for_vol, phi_opt_transformation_for_vol = rs.optimize(
        target_function = lambda actual_value, actual_transformation:
            phi_optimize_target_function(
            actual_value,
            actual_transformation,
            vol_opt_transformation.inverse()
            ),
        return_transformation_also=True
    )
    properties_to_add['optimize:phi_opt_transformation_for_vol'] = json_dumps_prop(phi_opt_transformation_for_vol)
    t.measure_time('optimize:vol_plus_phi:optimize')

    transform_matrix = phi_opt_transformation_for_vol * vol_opt_transformation.inverse()
    assert_equal(phi_opt_rs_for_vol.decide_gns(start_point_source=vol_opt_rs,point_transform=transform_matrix),is_gns, 'vol_plus_phi decide differs')
    t.measure_time('optimize:vol_plus_phi:decide')

    # Vol + VolPhi
    volphi_opt_rs, volphi_opt_transformation = vol_opt_rs.optimize(
        target_function = phi_optimize_target_function,
        return_transformation_also=True
    )
    properties_to_add['optimize:volphi_opt_transformation'] = json_dumps_prop(volphi_opt_transformation)
    t.measure_time('optimize:vol_plus_volphi:optimize')
    assert_equal(volphi_opt_rs.decide_gns(start_point_source=vol_opt_rs,point_transform=volphi_opt_transformation),is_gns, 'vol_plus_volphi decide differs')
    t.measure_time('optimize:vol_plus_volphi:decide')

    ##########################
    # Complex
    complex_opt_rs, complex_opt_transformation = rs.optimize(target_function=complex_target_function, return_transformation_also=true, timeout=1800)
    properties_to_add['optimize:complex_opt_transformation'] = json_dumps_prop(complex_opt_transformation)

    t.measure_time('optimize:complex:optimize')
    assert_equal(complex_opt_rs.decide_gns(),is_gns,'complex decide result differs')
    t.measure_time('optimize:complex:decide')

    # Complex + Phi
    phi_opt_rs_for_complex, phi_opt_transformation_for_complex = rs.optimize(
        target_function = lambda actual_value, actual_transformation:
            phi_optimize_target_function(
            actual_value,
            actual_transformation,
            complex_opt_transformation.inverse()
            ),
        return_transformation_also=True
    )
    properties_to_add['optimize:phi_opt_transformation_for_complex'] = json_dumps_prop(phi_opt_transformation_for_complex)
    t.measure_time('optimize:complex_plus_phi:optimize')

    transform_matrix = phi_opt_transformation_for_complex * complex_opt_transformation.inverse()
    assert_equal(phi_opt_rs_for_complex.decide_gns(start_point_source=complex_opt_rs,point_transform=transform_matrix),is_gns, 'complex_plus_phi decide differs')
    t.measure_time('optimize:complex_plus_phi:decide')

    # Complex + ComplexPhi
    complexphi_opt_rs, complexphi_opt_transformation = complex_opt_rs.optimize(
        target_function = phi_optimize_target_function,
        return_transformation_also=True
    )
    properties_to_add['optimize:complexphi_opt_transformation'] = json_dumps_prop(complexphi_opt_transformation)
    t.measure_time('optimize:complex_plus_complexphi:optimize')
    assert_equal(complexphi_opt_rs.decide_gns(start_point_source=complex_opt_rs,point_transform=complexphi_opt_transformation),is_gns, 'complex_plus_complexphi decide differs')
    t.measure_time('optimize:complex_plus_complexphi:decide')

    properties_to_add.update(t.get_data())
    properties_to_add['optimize:complex:volume'] = complex_opt_rs.get_cover_box_volume()

    properties_to_add['gns'] = 1 if is_gns else 0

    call_server_add_property(data['id'], properties_to_add)

