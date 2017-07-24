import shorttext
import elibb_get_threads as egt
from shorttext.utils import standard_text_preprocessor_1


def main():
    preprocessor1 = standard_text_preprocessor_1()
    wvmodel = shorttext.utils.load_word2vec_model('./GoogleNews-vectors-negative300.bin.gz')
    traindatasource = egt.get_submissions()
    if type(traindatasource) == str:
        trainclassdict = egt.read_from_sqlite(traindatasource)
    else:
        trainclassdict = traindatasource
    kmodel = shorttext.classifiers.frameworks.CLSTMWordEmbed(len(trainclassdict.keys()))
    classifier = shorttext.classifiers.VarNNEmbeddedVecClassifier(wvmodel)
    classifier.train(trainclassdict, kmodel)
    num_subs = 0
    print("Number of trained submissions:")
    for sub in trainclassdict.values():
        num_subs += len(sub)
    print(num_subs)
    print("Trained")
    print(classifier.score(preprocessor1("ELI5 Why is the sky red? I'm sure it is, don't tell me otherwise.")))
    print("Scored")
    classifier.save_compact_model('./nnlibvec_convnet_subdata.bin')

if __name__ == "__main__":
    main()
