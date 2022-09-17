from matplotlib import pyplot as plt


def show_data(title, data,name):
    y = data["大陆总计"].tolist()
    plt.plot(y, marker=".")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.ylabel(title, )
    plt.title("中国大陆".encode('GBK').decode('GBK'))

    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    plt.savefig("templates/"+name+".png")
    plt.show()
