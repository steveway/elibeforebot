import shorttext
import elibb_get_threads as egt


def main():
    wvmodel = shorttext.utils.load_word2vec_model('./GoogleNews-vectors-negative300.bin.gz')
    traindatasource = egt.get_submissions()
    if type(traindatasource) == str:
        trainclassdict = shorttext.data.retrieve_csvdata_as_dict(traindatasource)
    else:
        trainclassdict = traindatasource
    # trainclassdict = shorttext.data.subjectkeywords()
    kmodel = shorttext.classifiers.frameworks.CNNWordEmbed(len(trainclassdict.keys()))
    classifier = shorttext.classifiers.VarNNEmbeddedVecClassifier(wvmodel)
    classifier.train(trainclassdict, kmodel)
    classifier.score('artificial intelligence')
    classifier.save_compact_model('./nnlibvec_convnet_subdata.bin')

if __name__ == "__main__":
    main()
