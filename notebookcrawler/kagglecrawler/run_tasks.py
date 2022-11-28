from .tasks import longtime_add
import time
if __name__ == '__main__':
    url = ['https://www.kaggle.com/'] # change them to your ur list.
    for i in url:
        result = longtime_add.delay(i)
        print(f'Task result: {result.result}')