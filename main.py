import filecmp
import glob
import shutil
import os
from tkinter import *


from Analyzer import Analyzer

files = ''

root = Tk()
root.configure(bg='purple')
root.title("lr1")
root.geometry("1300x800")
entry = Entry()
text = Text(width=100, height=20)
label_1 = Label(text="", bg='purple', fg="white", justify='left')


def bd_button_handler():
    if need_refresh():
        path = '/home/natashks/Documents/EYAZIIS/EUAZIIS/EUAZIIS_1/docs/docs2'
        path_2 = '/home/natashks/Documents/EYAZIIS/EUAZIIS/EUAZIIS_1/docs/docs3'
        path_3 = '/home/natashks/Documents/EYAZIIS/EUAZIIS/EUAZIIS_1/docs/docs4'
        files_1 = glob.glob(path + '/*.txt')
        files_2 = glob.glob(path_2 + '/*.txt')
        files_3 = glob.glob(path_3 + '/*.txt')
        for file in files_1:
            name = os.path.basename(file)
            shutil.copyfile(file, 'BD/' + name)
        extra_files = set(os.listdir(path)).symmetric_difference(os.listdir(os.getcwd() + '/BD'))
        for file in extra_files:
            os.remove(os.getcwd() + '/BD/' + file)
        for file in files_2:
            name = os.path.basename(file)
            shutil.copyfile(file, 'BD/' + name)
        for file in files_3:
            name = os.path.basename(file)
            shutil.copyfile(file, 'BD/' + name)
        label_1["text"] = 'Информация загружена в БД'


def need_refresh():
    path_1 = '/home/natashks/Documents/EYAZIIS/EUAZIIS/EUAZIIS_1/docs/docs2'
    path_2 = '/home/natashks/Documents/EYAZIIS/EUAZIIS/EUAZIIS_1/docs/docs3'
    path_3 = '/home/natashks/Documents/EYAZIIS/EUAZIIS/EUAZIIS_1/docs/docs4'
    result = filecmp.cmpfiles(path_1, os.getcwd()+'/BD',
                              set(os.listdir(os.getcwd()+'/BD')).union(os.listdir(path_1)), shallow=True)
    result_2 = filecmp.cmpfiles(path_2, os.getcwd()+'/BD',
                                set(os.listdir(os.getcwd()+'/BD')).union(os.listdir(path_2)), shallow=True)
    result_3 = filecmp.cmpfiles(path_3, os.getcwd()+'/BD',
                                set(os.listdir(os.getcwd()+'/BD')).union(os.listdir(path_3)), shallow=True)

    label_1['text'] = os.getcwd()+'/BD'
    label_1['text'] = result[1], result[2], result_2[1], result_2[2], result_3[1], result_3[2]

    if len(result[2]) != 0:
        return True
    elif len(result[1]) != 0:
        return True
    elif len(result_2[2]) != 0:
        return True
    elif len(result_2[1]) != 0:
        return True
    elif len(result_3[2]) != 0:
        return True
    elif len(result_3[1]) != 0:
        return True
    else:
        return False


def correlation_button_handler():
    all_files = glob.glob('BD/*.txt')
    analyzer = Analyzer(all_files)
    analyzer.analyze(entry.get())
    result = [(i[0], round(i[2], 3)) for i in analyzer.cosines]
    label_1['text'] = result
    text.insert(1.0, analyzer.get_documents_as_str())


def exit_button_handler():
    quit()


def help_button():
    label_1['text'] = '     * Нажмите на кнопку "Загрузить тексты", чтобы поместить информацию в БД\n \
    * Если хотите посчитать корреляцию: введите слово в пустую строку и нажмите на кнопку "Вычислить корреляцию"\n \
    * Если хотите выйти, нажмите кнопку "Завершить программу"'


bd_btn = Button(text="Загрузить тексты", command=bd_button_handler, bg="purple", fg="white", height=2, width=20)
correlation_btn = Button(text="Вычислить корелляцию ", command=correlation_button_handler, bg="purple", fg="white", height=2, width=20)
quit_btn = Button(text="Завершить программу", command=exit_button_handler, bg="purple", fg="white", height=2, width=20)
help_btn = Button(text="Помощь", command=help_button, bg="purple", fg="white", height=2, width=20)


bd_btn.pack()
correlation_btn.pack()
quit_btn.pack()
help_btn.pack()

entry.pack(padx=8, pady=8)
label_1.pack(padx=10, pady=10)
text.pack()

root.mainloop()
