# -*- coding: utf-8 -*-
import os
LTP_DATA_DIR = '/home/yangsong/Downloads/ltp_data_v3.4.0'  # ltp模型目录的路径
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
srl_model_path = os.path.join(LTP_DATA_DIR, 'srl')  # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
import jieba
from pyltp import Postagger
from pyltp import Parser
from pyltp import NamedEntityRecognizer
from pyltp import SementicRoleLabeller
from pyltp import Segmentor

postagger = Postagger() # 初始化实例

def get_parsing(sentence):
    postagger.load(pos_model_path)  # 加载模型
    words=list(pyltp_cut(sentence)) #结巴分词
    postags = list(postagger.postag(words))  # 词性标注

    tmp=[str(k+1)+'-'+v for k,v in enumerate(words)]
    print('\t'.join(tmp))
    parser = Parser() # 初始化实例
    parser.load(par_model_path)  # 加载模型
    arcs = parser.parse(words, postags)  # 句法分析
    # for arc in arcs:
    #     if arc.relation=='SBV':
    #         name=

    print ("\t".join("%s-%d:%s" % (k+1,arc.head, arc.relation) for k,arc in enumerate(arcs)))
    parser.release()  # 释放模型
    return arcs

def get_name_entity(sentence):
    recognizer = NamedEntityRecognizer()  # 初始化实例
    recognizer.load(ner_model_path)  # 加载模型
    words = list(pyltp_cut(sentence))  # 结巴分词
    postags = list(postagger.postag(words))  # 词性标注
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    tmp=[str(k+1)+'-'+v for k,v in enumerate(netags)]
    print('\t'.join(tmp))
    recognizer.release()  # 释放模型

def get_srl(sentence):
    labeller = SementicRoleLabeller()  # 初始化实例
    labeller.load(srl_model_path)  # 加载模型
    words = list(pyltp_cut(sentence))  # pyltp分词
    postags = list(postagger.postag(words))  # 词性标注
    arcs=get_parsing(sentence)
    # arcs 使用依存句法分析的结果
    roles = labeller.label(words, postags, arcs)  # 语义角色标注

    # 打印结果
    for role in roles:
        print(role.index, "".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
        labeller.release()  # 释放模型
#pyltp中文分词
def pyltp_cut(sentence):

    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    words = segmentor.segment(sentence)  # 分
    segmentor.release()  # 释放模型
    return words

# text=['澳大利亚战略政策研究所负责人彼得·詹宁斯也指责称，基廷正在经历“特朗普时刻”——特朗普经常与美国的情报部门主管发生冲突','萨瑟斯表示所有的狗都受过专门的训练及经过严格评估','林瑞希认为，“平时我们老师上课不拘泥于课本，注重拓展，引导我们思考生物学科的前沿问题，而这正好符合牛津、剑桥的招生要求','一位同学对记者坦言大学期间从未拉过女孩子的手']
# text=['《环球报》称，该法令最初的目的是放松对收藏家与猎人的限制，但现在扩大到其他条款。新法令将普通公民购买枪支的弹药数量上限提高至每年5000发，此前这一上限是每年50发。博索纳罗在法令签署仪式上称，“我们打破了垄断”“你们以前不能进口，但现在这些都结束了”。另据法新社报道，当天在首都巴西利亚的一次集会上，博索纳罗还表示，“我一直说，公共安全从家里开始的。”']
# text=["《环球报》称，博索纳罗在1月的电视讲话中称，要让“好人”更容易持有枪支。“人民希望购买武器和弹药，现在我们不能对人民想要的东西说不”。"]
# text=['A股早在2013年6月就已纳入新兴市场指数的候选列表中，但此后几年，都因为配额分配、资本流动限制、资本利得税等所谓原因而遭否决，“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”,证监会分管国际合作的副主席方星海都在今年一月份的时候表示。']
text=['“中国与MSCI在股指期货上的观点存在分歧，中国并不急于加入MSCI全球指数”,证监会分管国际合作的副主席方星海都在今年一月份的时候表示。']
for t in text:
    get_parsing(t)
    get_name_entity(t)
    words = list(pyltp_cut(t))  # pyltp分词
    postags = list(postagger.postag(words))  # 词性标注
    pos=[str(k+1)+'-'+str(v) for k,v in enumerate(postags)]
    print(pos)



