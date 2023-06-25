import os
from threading import Thread
from PyQt5.QtWidgets import QFileDialog
import PyPDF2
from PDF_file_creator import PDF_file_creator
from heatmap_on_JPG import heatmap_on_JPG
from svm import svm_result, features_to_svm
from extract_features import features_results
from user import user
from PyQt5 import QtCore


def object_to_string(obj):
    if obj is None:
        return "No data on photo"

    def format_value(value):
        if isinstance(value, float):
            return "{:.6f}".format(value)
        elif isinstance(value, tuple):
            return "({}, {})".format("{:.6f}".format(value[0]), "{:.6f}".format(value[1]))
        else:
            return str(value)

    # Convert each object to a multi-line string.
    return (f'Mean Gaze Position: {format_value(obj["Mean Gaze Position"])}\n'
            f'Median Gaze Position: {format_value(obj["Median Gaze Position"])}\n'
            f'Skewness of Gaze Positions: {format_value(obj["Skewness of Gaze Positions"])}\n'
            f'Standard Deviation of Gaze Positions: {format_value(obj["Standard Deviation of Gaze Positions"])}\n'
            f'Range of Gaze Positions: {format_value(obj["Range of Gaze Positions"])}\n'
            f'Total Gaze Distance: {format_value(obj["Total Gaze Distance"])}\n'
            f'Number of Saccades: {format_value(obj["Number of Saccades"])}\n'
            f'Left Part Percentage: {format_value(obj["Left Part Percentage"])}\n'
            f'Right Part Percentage: {format_value(obj["Right Part Percentage"])}\n'
            f'Percentage of points inside boxes: {format_value(obj["Percentage of points inside boxes"])}\n'
            f'"Percentage of points inside eyes and mouth:{format_value(obj["Percentage of points inside eyes and mouth"])}\n'
            f'Variance of Gaze Positions: {format_value(obj["Variance of Gaze Positions"])}\n'
            f'Average Velocity: {format_value(obj["Average Velocity"])}\n'
            f'Angular Velocity: {format_value(obj["Angular Velocity"])}\n'
            f'Number of Fixations: {format_value(obj["Number of Fixations"])}\n'
            f'Average Fixation Duration: {format_value(obj["Average Fixation Duration"])}\n'
            f'Total Fixation Duration: {format_value(obj["Total Fixation Duration"])}\n'
            f'Fixation Dispersion: {format_value(obj["Fixation Dispersion"])}\n')


def create_PDF_result_file(user):
    # generator = PDF_file_creator('kaka ' + 'results form.pdf')
    # base_path = r'C:\Users\orsta\Desktop\capstone_partB\back\temp_user_heatmap_images'
    # # first page
    # array_objects = features_results("yair_5_Male_sd.txt")
    # text_list = [object_to_string(obj) for obj in array_objects]
    # text = text_list[0]
    # usern = user(name='or_', gender='Male_', age='28_', email='orstainer@gmail.com')
    # generator.add_first_page('Results From', usern, base_path, text)
    #
    # # Image paths for main part
    # image_paths = [base_path + str(i) + '.png' for i in range(2, 25)]
    # generator.add_images_with_text(image_paths, text_list)
    #
    # # add results
    # generator.add_last_page(['kaki ze taim', 'ani ohel kafot', 'mamamamama', 'A professional diagnosis recommended'])
    # generator.save(r'C:\Users\orsta\Desktop\capstone_partB\back\PDF_results\\')
    generator = PDF_file_creator(user.name + ' results form.pdf')

    # From front to back/temp_user_heatmap_images
    base_path = os.path.abspath(os.path.join('..', 'back', 'temp_user_heatmap_images'))

    # From front to back/gaze_data_textFiles
    user_data_path = os.path.join('..', 'back', 'gaze_data_textFiles',
                                  f"{user.name}_{user.age}_{user.gender}_{user.email}.txt")

    array_objects = features_results(os.path.abspath(user_data_path))

    result_grade = svm_result(features_to_svm(array_objects))

    text_list = [object_to_string(obj) for obj in array_objects]
    text = text_list[0]
    generator.add_first_page('Results Form', user, base_path, text)
    # Image paths for main part
    image_paths = [os.path.join(base_path, f"{i}.jpg") for i in range(2, 25)]

    print("Process pdf..")
    generator.add_images_with_text(image_paths, text_list)
    # add results
    generator.add_last_page(['As our system found out', 'Your grade: ' + str(result_grade)])
    path_to_save = os.path.abspath(os.path.join('..', 'back', 'PDF_results'))
    generator.save(path_to_save)


def create_user_costume_heatmap_images(filename):
    # create new heatmap images based on the results
    heatmap_handler = heatmap_on_JPG(filename)
    process_data = heatmap_handler.processed_data
    [heatmap_handler.heatmap_on_image(index, process_data) for index in range(0, 24)]


def start_PDF_compose_process(mw, user):
    # step1: create new heatmap images based on the results
    create_user_costume_heatmap_images(filename=user.name + '_' + user.age + '_' + user.gender + '_' + user.email + '.txt')

    # step2: create PDF result file using the SVM classification
    create_PDF_result_file(user)

    # step3: send an email with the PDF attached to it

    # step4: apply the download PDF button to the file created

    # step5: signal the main thread (main window) that the work is done and the loading label can be hide
    QtCore.QMetaObject.invokeMethod(mw, "PDF_file_created", QtCore.Qt.QueuedConnection)


def init_result_info_screen(mw):
    print("Init result info screen..")
    # change screen page
    mw.ui.screens_stack.setCurrentIndex(3)

    # change label name to the given email
    mw.ui.email_sent_label.setText(mw.ui.email_sent_label.text() + str(mw.ui.email_lineEdit.text()))

    # hide the object on the screen until calculations are done
    mw.ui.main_menu_btn.hide()
    mw.ui.results_frame.hide()

    # show loading gif to indicate the user calculations are made
    mw.ui.label.show()

    # start the process to create the PDF file should work on a thread
    current_user = user(gender=mw.ui.gender_cb.currentText(), age=mw.ui.age_lineEdit.text(), name=mw.ui.name_lineEdit.text(), email=mw.ui.email_lineEdit.text())
    thread = Thread(target=start_PDF_compose_process, args=(mw, current_user,))
    thread.start()


# Clicking download pdf button event
def download_PDF(mw):

    # open the file dialog to choose the save directory
    suggested_name = mw.ui.name_lineEdit.text() + ' results form'
    file_name, _ = QFileDialog.getSaveFileName(None, "Save File", suggested_name, "PDF Files (*.pdf)")

    # check if the user has chosen a directory
    if file_name:

        # set the path to the file to be downloaded
        file_path = 'back/PDF_results/'
        file_path += mw.ui.name_lineEdit.text() + '_'
        file_path += mw.ui.age_lineEdit.text() + '_'
        file_path += mw.ui.gender_cb.currentText() + '_'
        file_path += mw.ui.email_lineEdit.text() + '.pdf'

        # Open the PDF file
        with open('\\back\\PDF_results\\' + suggested_name, 'rb') as pdf_file:
            # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create a PdfFileWriter object
        pdf_writer = PyPDF2.PdfWriter()

        # Add the modified PDF contents to the writer
        pdf_writer.addPage(pdf_reader.pages[0])

        # Save the modified PDF to the given path
        with open(file_name, 'wb') as output_file:
            pdf_writer.write(output_file)


# user1 = user(name='Dvir', age='4', gender='Male', email='Dvirvahav@gmail.com')
# create_user_costume_heatmap_images(filename=user1.name + '_' + user1.age + '_' + user1.gender + '_' + user1.email + '.txt')
# create_PDF_result_file(user1)