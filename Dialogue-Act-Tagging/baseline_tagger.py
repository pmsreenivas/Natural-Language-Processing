import pycrfsuite as crf
import  hw2_corpus_tools as hct
import sys
import os

input_directory = str(sys.argv[1])
test_directory = str(sys.argv[2])
output_file = str(sys.argv[3])

gen_input = hct.get_data(input_directory)
gen_test = hct.get_data(test_directory)

master_list_input = []
master_list_test = []

while True:
    try:
        master_list_input.append(gen_input.__next__())
    except StopIteration:
        break

while True:
    try:
        master_list_test.append(gen_test.__next__())
    except StopIteration:
        break

trainer = crf.Trainer(verbose=False)

feature_vector_list = []
utterance_vector = []
label_list = []

for dialogue in master_list_input:
    for utterance in dialogue:
        label_list.append(utterance.act_tag)
        idx = dialogue.index(utterance)
        if idx == 0:
            utterance_vector.append("FIRST_UTTERANCE")
        else:
            curr_speaker = utterance.speaker
            prev_speaker = dialogue[idx - 1].speaker
            if curr_speaker != prev_speaker:
                utterance_vector.append("SPEAKER_CHANGED")
        if utterance.pos is None:
            utterance_vector.append("NO_WORDS")
        else:
            for token, pos in utterance.pos:
                utterance_vector.append("TOKEN_" + token)
                utterance_vector.append("POS_" + pos)
        feature_vector_list.append(utterance_vector[:])
        utterance_vector.clear()
    trainer.append(feature_vector_list, label_list)
    feature_vector_list.clear()
    utterance_vector.clear()
    label_list.clear()

trainer.set_params({
    'c1': 1.0,
    'c2': 1e-3,
    'max_iterations': 50,
    'feature.possible_transitions': True
})


trainer.train("model.crfsuite")


tagger = crf.Tagger()
tagger.open("model.crfsuite")

f = open(output_file, "w")
g = open("accuracy_apple_carrot.txt", "w")

dev = True

if master_list_test[0][0].act_tag is not None:
    dev = True

for dialogue in master_list_test:
    for utterance in dialogue:
        label_list.append(utterance.act_tag)
        idx = dialogue.index(utterance)
        if idx == 0:
            utterance_vector.append("FIRST_UTTERANCE")
        else:
            curr_speaker = utterance.speaker
            prev_speaker = dialogue[idx - 1].speaker
            if curr_speaker != prev_speaker:
                utterance_vector.append("SPEAKER_CHANGED")
        if utterance.pos is None:
            utterance_vector.append("NO_WORDS")
        else:
            for token, pos in utterance.pos:
                utterance_vector.append("TOKEN_" + token)
                utterance_vector.append("POS_" + pos)
        feature_vector_list.append(utterance_vector[:])
        utterance_vector.clear()
    pred = tagger.tag(feature_vector_list)
    for i in range(len(pred)):
        f.write(pred[i] + "\n")
        if dev:
            g.write(pred[i] + " " +label_list[i] + "\n")

    feature_vector_list.clear()
    utterance_vector.clear()
    label_list.clear()
    f.write("\n")

f.close()
g.close()

