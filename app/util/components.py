from threading import Thread


def async(f):
    """
    @decorator 异步执行
    :param f:
    :return:
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def console_out(message, file_name):
    """
    输出信息
    :param message:
    :param file_name: 文件名
    :return:
    """
    print(message)

    with open(file_name, 'a', encoding='utf-8') as file:
        file.writelines(message + '\n')


if __name__ == '__main__':
    console_out('你好', '../tmp/console.txt')
