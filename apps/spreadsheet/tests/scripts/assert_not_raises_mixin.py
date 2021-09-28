class AssertNotRaisesMixin:

    def assertNotRaises(self, callable):
        try:
            callable()
        except Exception as e:
            self.assertTrue(False, msg=f'Exception of type: "{type(e).__name__}" was thrown')
        self.assertTrue(True)
