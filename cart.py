import random
from collections import Counter
class condition(object):
    def __init__(self, attr_id, value):
        self.attr_id = attr_id
        self.value = value
        self.num_mode = isinstance(self.value, float) or isinstance(self.value, int)
    def __str__(self):
        comparator = ">=" if self.num_mode else "=="
        return "Атрибут {} {} {}:".format(self.attr_id + 1, comparator, self.value)
    def answer(self, instance):
        if self.num_mode:
            return instance[self.attr_id] >= self.value
        else:
            return instance[self.attr_id] == self.value

class node(object):
    def __init__(self, cond, true_subtree, false_subtree):
        self.cond = cond
        self.true_sub = true_subtree
        self.false_sub = false_subtree
    def print_tree(self, offset = 0):
        padding = "\n" + offset * "\t\t" + "\____"
        q = str(self.cond)
        true = padding + "Так:" + self.true_sub.print_tree( offset=offset + 1)
        false = padding + "Ні:" + self.false_sub.print_tree( offset=offset + 1)
        return q + true + false
    def classify(self, instance):
        if self.cond.answer(instance):
            return self.true_sub.classify(instance)
        else:
            return self.false_sub.classify(instance)

class leaf(object):
    def __init__(self, data):
        self.probabil = self.class_frequency(data)

    @staticmethod
    def class_frequency(data):
        classes = [row[-1] for row in data]

        return Counter(classes)

    def print_tree(self, offset=0):
        total_count = sum(self.probabil.values())
        results = {}
        for class_name, count in self.probabil.items():
            results[class_name] = count * 100 / total_count
        return  ",".join(["{} - {}".format(r[0], r[1]) for r in results.items()])

    def classify(self, _):
        return self.probabil

class cart_tree(object):
    def __init__(self, data):
        self.tree = self.create_tree(data)
    @staticmethod
    def calc_uncertainty(data):
        uncer = 1
        count_of_labels = Counter([row[-1] for row in data])
        num_instances = len(data)
        for label, count in count_of_labels.items():
            prob_of_matching = (count/num_instances)**2
            uncer -= prob_of_matching
        return uncer
    def calc_info_gain(self, lhs_data, rhs_data, cur_uncert):
        num_instances = len(lhs_data) + len(rhs_data)
        uncert_lhs = self.calc_uncertainty(lhs_data)
        uncert_rhs = self.calc_uncertainty(rhs_data)
        weight_lhs = len(lhs_data)/num_instances
        weight_rhs = len(rhs_data)/num_instances
        new_uncert = weight_lhs*uncert_lhs + weight_rhs*uncert_rhs
        return cur_uncert - new_uncert

    @staticmethod
    def calc_unique_values(data, attr_id):
        values = [instance[attr_id] for instance in data]

        unique_values = set(values)
        return unique_values

    def calc_best_split(self, data):
        best_info_gain = 0

        best_cond = None
        for attr_id in range(len(data[0]) - 1):
            for val in self.calc_unique_values(data, attr_id):
                cond = condition(attr_id, val)
                true_instances, false_instances = self.split_data(data, cond)
                if max(len(true_instances), len(false_instances)) >= len(data):
                    continue
                info_gain = self.calc_info_gain(false_instances,
                                                true_instances, self.calc_uncertainty(data))
                if info_gain > best_info_gain:
                    best_info_gain = info_gain
                best_cond = cond
        return best_info_gain, best_cond

    @staticmethod
    def split_data(data, cond):
        true_data = [row for row in data if cond.answer(row)]

        false_data = [row for row in data if not cond.answer(row)]
        return true_data, false_data

    def create_tree(self, data):
        info_gain, cond = self.calc_best_split(data)

        if info_gain == 0:
            return leaf(data)
        true_data, false_data = self.split_data(data, cond)
        true_subtree = self.create_tree(true_data)

        false_subtree = self.create_tree(false_data)
        return node(cond, true_subtree, false_subtree)

    def print_tree(self):
        print( "" )
        print(self.tree.print_tree())
        print("")

        def classify(self, instance):
            result_counts = self.tree.classify(instance)

            results = []
            for class_name, count in result_counts.items():
                results += [class_name] * count
            return random.choice(results)

        def test_accuracy(self, test_data):
            num_correct = 0

            for instance in test_data:
                answer = self.classify(instance[0:-1])
            if answer == instance[-1]:
                num_correct += 1
            return num_correct / len(test_data)

        def save(self, test_data):
            with open("results.csv ", mode= "") as file:
                for instance in test_data:
                    answer = self.classify(instance[0:-1])
                    row = "".join([str(i) for i in instance] + [answer])
                    file.write(row + "\n")
