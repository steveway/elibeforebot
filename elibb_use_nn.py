import shorttext
# import elibb_get_threads as egt
from shorttext.utils import standard_text_preprocessor_1


def main():
    preprocessor1 = standard_text_preprocessor_1()
    wvmodel = shorttext.utils.load_word2vec_model('./GoogleNews-vectors-negative300.bin.gz')
    classifier = shorttext.classifiers.load_varnnlibvec_classifier(wvmodel, './nnlibvec_convnet_subdata.bin')
    print(classifier.score(preprocessor1("ELI5 Why is the sky red? I'm sure it is, don't tell me otherwise.")))
    print("Scored")


if __name__ == "__main__":
    main()
