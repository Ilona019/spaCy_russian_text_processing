import codecs
import spacy
from spacy.matcher import Matcher
import re

# Арефьева Илона Юрьевна ИВТ-21МО. Анализ рассказа А.П. Чехова "Огни" с помощью библиотеки Spacy.


# Удаляем знаки препинания и пробельные символы вокруг из строки
def remove_punctuation_marks(sent):
    return re.sub(r'[^\w\s]', '', sent).strip()+'.'


# Запись результатов в файл result.txt
def writing_line_in_file(line):
    file.write(line)


file = codecs.open( "text.txt", "r", "utf_8_sig" )
text = file.read()
file.close()

nlp = spacy.load("ru_core_news_sm")
doc = nlp(text)
# doc.sents — объект-генератор — не индексируется, поэтому преобразуем в список
sents = list(doc.sents)
word_count = 0
number_of_punctuation_marks = 0
number_of_nouns = 0
number_of_verbs = 0
for token in doc:
    if not token.is_punct:
        word_count += 1
    if token.pos_ == 'PUNCT':
        number_of_punctuation_marks += 1
    elif token.pos_ == 'NOUN':
        number_of_nouns += 1
    elif token.pos_ == 'VERB':
        number_of_verbs += 1

print(f'а) Количество слов в тексте: {word_count}')
file = open('result.txt', 'w')
writing_line_in_file(f'а) Количество слов в тексте: {word_count}\n')
print(f'б) Количество предложений в тексте: {len(sents)}')
writing_line_in_file(f'б) Количество предложений в тексте: {len(sents)}\n')
print(f'в) Количество знаков пунктуации в тексте: {number_of_punctuation_marks}')
writing_line_in_file(f'в) Количество знаков пунктуации в тексте: {number_of_punctuation_marks}\n')
print(f'г) Доля существительных {number_of_nouns/word_count}; \n'
      f' Доля глаголов: {number_of_verbs/word_count} относительно всех слов текста')
writing_line_in_file(f'г) Доля существительных {number_of_nouns/word_count}; \n'
      f' Доля глаголов: {number_of_verbs/word_count} относительно всех слов текста\n')

word = input('Введите слово для поиска предложений в тексте: ')
doc_input_word = nlp(word)
input_word_lemma = doc_input_word[0].lemma_
print(f'Лемма: {input_word_lemma}')
print(f'д) Предложения, в которых встречается слово {doc_input_word.text}')
writing_line_in_file(f'д) Предложения, в которых встречается слово {doc_input_word.text}\n')
count = 0
for sent in doc.sents:
    for token in sent:
        if token.lemma_ == input_word_lemma:
            count += 1
            print(str(count)+')', sent)
            writing_line_in_file(str(count)+')'+sent.text+'\n')
            break

unique_lemmas = set()
for token in doc:
    if not token.is_punct and token.lemma_ not in unique_lemmas:
        unique_lemmas.add(token.lemma_)

print(f'е) Количество различных слов в тексте: {len(unique_lemmas)}')
writing_line_in_file(f'е) Количество различных слов в тексте: {len(unique_lemmas)}\n')
print('ж) Предложения, которые начинаются и заканчиваются на одно и тоже слово:')
writing_line_in_file('ж) Предложения, которые начинаются и заканчиваются на одно и тоже слово:\n')
matcher = Matcher(nlp.vocab, validate=True)
for sent in doc.sents:
    clear_str = remove_punctuation_marks(sent.text)
    lemma_first_word = nlp(clear_str.split(' ')[0].strip())[0].lemma_
    pattern = [{'LEMMA': lemma_first_word, 'IS_SENT_START': True}, {'IS_SENT_START': False, 'OP': '*'}, {'LEMMA': lemma_first_word, 'IS_SENT_START': False}, {'TEXT': {'REGEX': '[.]$'}}]
    matcher.add("sent_start_end_same_word", [pattern])
    doc1 = nlp(clear_str)
    matches = matcher(doc1)
    if len(matches) >= 1:
        print(sent)
        file.write(sent.text+'\n')

print('з) Пары предложений, которые начинаются одним и тем же словом или словосочетанием:')
writing_line_in_file('з) Пары предложений, которые начинаются одним и тем же словом или словосочетанием:\n')
dictionary_sents = {}
for index in range(0, len(sents)):
    # Удалим знаки препинания, кавычки, которые мешают выделить первое слово.
    clear_str = remove_punctuation_marks(sents[index].text)
    # Берем лемму нового слова
    lemma_first_word = nlp(clear_str.split(' ')[0].strip())[0].lemma_
    if lemma_first_word in dictionary_sents:
        print(f'Пара № {index}')
        print(dictionary_sents[lemma_first_word])
        print(sents[index].text, '\n')
        file.write(f'---Пара № {index}---\n')
        file.write(f'{dictionary_sents[lemma_first_word]}\n')
        file.write(f'{sents[index].text}\n')
        dictionary_sents.pop(lemma_first_word)
    else:
        dictionary_sents[lemma_first_word] = sents[index].text

file.close()
