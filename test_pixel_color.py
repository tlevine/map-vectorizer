import nose.tools as n

from pixel_color import old_color, new_color

def test_old():
    n.assert_tuple_equal(old_color('dsv-truck.jpg'), (114, 130, 131))

def test_new():
    n.assert_tuple_equal(new_color('dsv-truck.jpg'), (86, 146, 200))
