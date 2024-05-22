from apps.tests.models import Test


class TestRepository:
    def create_test(self, name, description, type):
        test = Test(name=name, description=description, type=type)
        test.save()
        return test

    def update_test(self, test_id, name=None, description=None, type=None):
        test = Test.objects.get(id=test_id)
        if name is not None:
            test.name = name
        if description is not None:
            test.description = description
        if type is not None:
            test.type = type
        test.save()
        return test

    def delete_test(self, test_id):
        test = Test.objects.get(id=test_id)
        test.delete()

    def get_test(self, test_id):
        return Test.objects.get(id=test_id)

    def get_all_tests(self):
        return Test.objects.all()
