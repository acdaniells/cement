from cement.core.output import OutputHandler, OutputInterface

# module tests


class TestOutputInterface:
    def test_interface(self):
        assert OutputInterface.Meta.interface == "output"


class TestOutputHandler:
    def test_subclassing(self):
        class MyOutputHandler(OutputHandler):
            class Meta:
                label = "my_output_handler"

            def render(self, *args, **kw):
                pass

        h = MyOutputHandler()
        assert h._meta.interface == "output"
        assert h._meta.label == "my_output_handler"


# app functionality and coverage tests

TEST_TEMPLATE = "%(foo)s"
