
import os
import pickle



def generate_train_dict(questions,answers,max_length):

	words = set()
	questions = [q.split()[-max_length:] for q in questions]
	answers = [a.split()[:max_length] for a in answers]

	for q in questions:
		words.update(q)

	for a in answers:
		words.update(a)

	id2word = {x:num+4 for x,num in enumerate(words)}
	word2id = {num+4:x for x,num in enumerate(words)}

	special_words = ['<pad>', '<go>', '<eos>', '<unknown>']
	id2word = id2word.update({x:num for x,num in enumerate(special_words)})
	word2id = word2id.update({num:x for x,num in enumerate(special_words)})

	train_data = []
	for q,a in zip(questions,answers):
		train_data.append([[word2id(x) for x in q],[word2id(y) for y in a]])

	train_dict = {
		'train_samples': train_data,
		'word2id': word2id,
		'id2word': id2word
	}

	return train_dict


def get_question_and_answers(ans_filename,ques_filename):

	questions = []
	answers = []
	with open(ques_filename,"r") as f:
		questions = [x for x in f.read().split("\n")]

	with open(ans_filename,"r") as f:
		answers = [x for x in f.read().split("\n")]

	return questions,answers

def create_train_pickle(ans_filename,ques_filename,max_length):
	questions,answers = get_question_and_answers(ans_filename,ques_filename)
	train_dict = generate_train_dict(questions,answers,max_length)
	with open('train_file.pkl','wb') as pkl:
		pickle.dump(train_dict,pkl)

	print("File saved")	

