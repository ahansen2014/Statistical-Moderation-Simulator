'''
VCAA STAT MOD simulator ver 0.2
This application has been developed privately and is designed to allow teachers to simulate an approximate
stat mod process.  The simulation does fix the zero, first quartile, median, third quartile and top reference points
as described in VCAA documents, however, it uses a linear mapping for the scores between these points and therefore
the resulting moderated scores are an approximation only. In real stat mod smoothing algorithms would be used to
smooth the data.  This has not been done in this simulation.

(C) Andrew R. Hansen. 8th May 2022

Changelog:
Version 0.2, 10/5/22, updated exam top calc to account for multiple students with the same top SAC score but different
exam scores.
'''
from tkinter import *
from numpy import quantile, mean

# Some initial arrays to provide initial data.  The names are from a random name generator.
names = ['Aydin Mata', 'Nico Horton', 'Georgie Burgess', 'Natalie Atkinson', 'Lexie Vaughn', 'Augustus Summers',
         'Joyce Stephenson', 'Lyric Bryant', 'Austin Owens', 'Colten Walsh', 'Amari Tanner', 'Julie Patrick',
         'Jaydon Dean', 'Kassandra Mcconnell', 'Travis Riggs', 'Leonidas Meadows', 'Yasmine Bowman',
         'Omari Vaughan', 'Peter Hudson', 'Randy Lam', 'Charles Warren', 'Camryn Garcia', 'Jamir Baker',
         'Harley Crawford', 'Ashtyn Lucas']

sac_scores = [95, 92, 85, 83, 78, 75, 68, 66, 65, 61, 60, 59, 58, 55, 52, 51, 50, 45, 41, 39, 36, 34, 32, 31, 25]
mod_scores = [95, 92, 85, 83, 78, 75, 68, 66, 65, 61, 60, 59, 58, 55, 52, 51, 50, 45, 41, 39, 36, 34, 32, 31, 25]
exam_scores = [96, 95, 91, 87, 83, 82, 77, 75, 74, 70, 68, 67, 66, 65, 63, 61, 60, 58, 57, 56, 54, 53, 52, 51, 51]

# Arrays to hold the UI elements.  It's nice that Python allows arrays to hold objects like UI elements
number_labels = []
name_labels = []
sac_entrys = []
mod_labels = []
exam_entrys = []

def find_exam_top(sac_scores, exam_scores):
    '''
    If there are multiple students with the same top SAC score then that score is mapped to the average of the top exam
    scores.  That is, if there are three students with the same top SAC score then their score will be mapped to the
    average of the top three exam scores.
    :param sac_scores: The list of raw SAC scores
    :param exam_scores: The list of exam scores
    :return: the average of the N top exam scores
    '''
    biggest = 0
    occurrence = 0

    for score in sac_scores:
        if score > biggest:
            biggest = score
            occurrence = 1
        elif score == biggest:
            occurrence += 1

    top_exam_scores = []

    for score in exam_scores:
        if len(top_exam_scores) < occurrence:
            top_exam_scores.append(score)
        else:
            if score > min(top_exam_scores): #  If the score is bigger than the smallest in the list ...
                top_exam_scores.remove(min(top_exam_scores)) #  ... remove the smallest ...
                top_exam_scores.append(score) #  ... and replace it with the new one.
    exam_top = mean(top_exam_scores)

    return exam_top

def map_scores(I_range_min, I_range_max, F_range_min, F_range_max, I_score):
    '''
    This is the mapping function that maps unmoderated SAC scores against the exam scores.  The mapping in linear and
    therefore the formula is unique to each range.  The formula used is:
    score[mod] = (Range[exam]/Range[SAC]) * (score[sac] - SAC[min]) + exam[min]
    The square brackets here are being used in place of a subscript notation.
    :param I_range_min: Lower boundary score for the initial (or SAC) scores range
    :param I_range_max: Upper boundary score for the initial (or SAC) scores range
    :param F_range_min: Lower boundary score for the final (or exam) scores range
    :param F_range_max: Upper boundary score for the final (or exam) scores range
    :param I_score: Initial (or SAC) score to be moderated
    :return: Moderated score
    '''
    if I_score < I_range_min or I_score > I_range_max: # Not sure we need this but an ounce of prevention ...
        print('Initial score invalid.  Out of range.')
        return None
    else:
        F_score = round(((F_range_max - F_range_min) / (I_range_max - I_range_min)) * (I_score - I_range_min) + F_range_min)
        return F_score

def calc_moderated_score(sac_scores, exam_scores):
    '''
    This function is deliberately clunky to allow the process to more closely model the process described by the VCAA
    in their published documents.  That process is, first map the zero, first quartile, median, third quartile and top
    scores points then map between them.
    :param sac_scores: Internal, unmoderated scores
    :param exam_scores: External scores to be moderated against.
    :return: Updated moderated scores array.
    '''
    sac_zero = 0
    sac_25 = quantile(sac_scores, 0.25)
    sac_50 = quantile(sac_scores, .5)
    sac_75 = quantile(sac_scores, 0.75)
    sac_top = quantile(sac_scores, 1)

    exam_zero = 0
    exam_25 = quantile(exam_scores, 0.25)
    exam_50 = quantile(exam_scores, .5)
    exam_75 = quantile(exam_scores, 0.75)
    exam_top = find_exam_top(sac_scores, exam_scores)

    for i in range(25):
        # first, explicitly map the quartiles
        if sac_scores[i] == sac_zero:
            mod_score = exam_zero
        elif sac_scores[i] == sac_25:
            mod_score = exam_25
        elif sac_scores[i] == sac_50:
            mod_score = exam_50
        elif sac_scores[i] == sac_75:
            mod_score = exam_75
        elif sac_scores[i] == sac_top:
            mod_score = exam_top
        # Now map the scores in between
        elif sac_scores[i] > sac_zero and sac_scores[i] < sac_25:
            mod_score = map_scores(sac_zero, sac_25, exam_zero, exam_25, sac_scores[i])
        elif sac_scores[i] > sac_25 and sac_scores[i] < sac_50:
            mod_score = map_scores(sac_25, sac_50, exam_25, exam_50, sac_scores[i])
        elif sac_scores[i] > sac_50 and sac_scores[i] < sac_75:
            mod_score = map_scores(sac_50, sac_75, exam_50, exam_75, sac_scores[i])
        elif sac_scores[i] > sac_75 and sac_scores[i] < sac_top:
            mod_score = map_scores(sac_75, sac_top, exam_75, exam_top, sac_scores[i])
        else:
            mod_score = 0 # We don't need this but, it removes a warning about referencing a variable before assignment

        mod_scores[i] = int(mod_score)


def calculate():
    # Update score arrays based on UI data
    for i in range(25):
        sac_scores[i] = int(sac_entrys[i].get())
        exam_scores[i] = int(exam_entrys[i].get())

    # Update the moderated scores array based on new SAC / exam data
    calc_moderated_score(sac_scores, exam_scores)

    # Copy the new moderated scores to the UI
    for i in range(25):
        mod_labels[i].config(text=str(mod_scores[i]))



main = Tk()
main.title('Stat Mod Simulator v0.2')
main.geometry('500x900+200+100')

space1 = Label(main, text='     ').grid(row=0, column=0)
space2 = Label(main, text='     ').grid(row=2, column=0)
space3 = Label(main, text='     ').grid(row=28, column=0)

num_label = Label(main, text='No.').grid(row=1, column=1)
name_label = Label(main, text='Name').grid(row=1, column=2)
sac_label = Label(main, text='SAC score').grid(row=1, column=3)
mod_label = Label(main, text='SAC moderated').grid(row=1, column=4)
exam_label = Label(main, text='Exam score').grid(row=1, column=5)

for i in range(25):
    number_labels.append(Label(main, text=str(i+1)))
    number_labels[i].grid(row=i+3, column=1)
    name_labels.append(Label(main, text=names[i]))
    name_labels[i].grid(row=i+3, column=2)
    sac_entrys.append(Entry(main, width=5))
    sac_entrys[i].grid(row=i+3, column=3)
    sac_entrys[i].delete(0, END)
    sac_entrys[i].insert(0, str(sac_scores[i]))
    mod_labels.append(Label(main, text=str(mod_scores[i])))
    mod_labels[i].grid(row=i+3, column=4)
    exam_entrys.append(Entry(main, width=5))
    exam_entrys[i].grid(row=i + 3, column=5)
    exam_entrys[i].delete(0, END)
    exam_entrys[i].insert(0, str(exam_scores[i]))

calc_button = Button(main, text='Calculate', command=calculate)
calc_button.grid(row=29, column=2)

mainloop()