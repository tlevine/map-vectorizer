import nose.tools as n

from pixel_color import old_color, new_color

def test_old():
    n.assert_tuple_equal(old_color('dsv-truck.jpg'), (114, 130, 131))
