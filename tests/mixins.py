# coding: utf-8


class ParserTestCaseMixin(object):

    maxDiff = None

    def assertRaisesWithMessage(self, exception_type, message, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exception_type as e:
            self.assertEqual(e.args[0], message)
        else:
            self.fail(
                '"{:}" was expected to throw "{:}" exception'
                .format(func.__name__, exception_type.__name__))


class StructureTestCaseMixin(object):

    def assertStructure(self, structure_class, **kwargs):
        structure_a = structure_class(**kwargs)

        for key in kwargs.keys():
            self.assertEqual(
                getattr(structure_a, key),
                kwargs[key]
            )

        structure_b = structure_class(**kwargs)

        self.assertNotEqual(id(structure_a), id(structure_b))
        self.assertEqual(structure_a, structure_b)
