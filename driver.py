import random
from statistics import mean, stdev
from cart import cart_tree
def recording(path):
    with open(path) as file:
        input = file.readlines()
        data = []
    for entry in input:
        readings = entry.rstrip("\n").split("")
        attributes = [float(r) for r in readings[0:-1]]
        attributes.append(readings[-1])
        data.append(attributes)
    return data

def main():
    path_to = input("Введіть шлях до вибірки :")
    data = recording(path_to)
    cart_tree(data).print_tree()
    scores = []
    for i in range(0,10):
        random.shuffle(data)
        train_n = len(data) * 2//3
        training_data = data[0:train_n]
        test_data = data[train_n:]
        cart = cart_tree(training_data)
        accuracy = cart.test_accuracy(test_data)
        print("Ітерація - {}, Точність - {:.4f}".format(i+1, accuracy))
        scores.append(accuracy)
        cart.save(test_data)
        print("")
        print("Класифікатор CART має точність {:.2f}%, +/- {:.2f}".format(mean(scores) * 100, stdev(scores) * 2 * 100))
if __name__ == "__main__":
    main()