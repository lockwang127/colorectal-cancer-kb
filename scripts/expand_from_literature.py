#!/usr/bin/env python3
"""
知识库延展脚本 - 整合英文外科学资源和专业书籍内容
将外部文献内容转化为中文知识三元组并入库
"""

import json
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
KB_PATH = str(BASE_DIR / "data" / "knowledge-graph" / "relations.json")

# ========== 第一批：TME（直肠系膜切除术）============

TME_TRIPLETS = [
    # 历史与基础
    {"head": "直肠系膜切除术(TME)", "relation": "历史地位", "tail": "直肠系膜切除术(TME)是直肠癌根治性切除的金标准，由Heald于1979年系统化推广", "source": "Knol J, Keller DS. Total Mesorectal Excision Technique—Past, Present, and Future. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME", "relation": "历史起源", "tail": "TME概念最早由Richard Heald教授于1979年系统化提出，此前Abel于1931年首次描述了该手术", "source": "Knol J, Keller DS. Total Mesorectal Excision Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "专家共识", "domain": "外科手术"},
    {"head": "Miles APR术", "relation": "历史地位", "tail": "1908年William Ernest Miles提出腹会阴联合切除术(APR)，将直肠癌局部复发率从近100%降至约30%", "source": "Miles WE. Lancet 1908", "evidence": "专家共识", "domain": "外科手术"},
    {"head": "直肠系膜", "relation": "解剖定义", "tail": "直肠系膜来源于胚胎期后肠肠系膜，由结缔组织和脂肪构成，包含血管和淋巴供应，被筋膜系统包绕", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "直肠分段", "relation": "解剖标准", "tail": "上段直肠: 距肛缘12-15cm；中段直肠: 7-12cm；下段直肠: 0-7cm", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "分期系统"},
    {"head": "直肠固有筋膜", "relation": "解剖意义", "tail": "直肠固有筋膜(Fascia Propria)是贴附直肠的薄透明脏层筋膜，维持直肠系膜完整性，TME术中需保持其完整", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "骶前筋膜", "relation": "解剖意义", "tail": "骶前筋膜(Presacral Fascia)是壁层筋膜，位于直肠系膜后方，覆盖骶骨凹面和骶前静脉，TME术中需保持完整避免骶前大出血", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "Denonvilliers筋膜", "relation": "解剖特点", "tail": "Denonvilliers筋膜是位于直肠前方的坚韧纤维双层组织，分隔直肠与前列腺/精囊腺(男性)或阴道后壁(女性)，男性中更发达，大多数TME术中不切除", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "Waldeyer筋膜", "relation": "解剖特点", "tail": "直肠骶骨韧带(Waldeyer筋膜)在第3-4骶椎水平由直肠系膜与骶前筋膜融合形成，是直肠后方锚定筋膜，TME术中必须锐性切断", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "直肠血供", "relation": "静脉回流特点", "tail": "直肠上2/3经直肠上静脉→门静脉循环(肝转移)；下1/3经直肠中、下静脉→髂内静脉→体循环(肺转移)", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "腹下神经", "relation": "自主神经功能", "tail": "交感神经(T12-L2)沿直肠系膜后方走行至盆壁，负责尿液控制和射精功能，IMA结扎或系膜游离时损伤可致尿失禁和逆行射精", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "盆神经丛", "relation": "自主神经功能", "tail": "副交感神经(S2-S4)沿直肠系膜筋膜外侧和前方走行，与腹下神经汇合形成下腹下丛，负责排尿、勃起和润滑功能，外侧或前方游离时损伤致勃起困难和尿潴留", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},

    # 适应证与切缘
    {"head": "TME", "relation": "手术适应证", "tail": "TME是中段和下段直肠肿瘤根治性切除的明确适应证，作为低位前切除术(LAR)或腹会阴切除术(APR)的一部分进行", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "肿瘤特异性直肠系膜切除", "relation": "适应证", "tail": "上段直肠癌或肿瘤距肛缘超过10cm时，远端切缘可达5cm，可行肿瘤特异性直肠系膜切除，效果与完整TME相当", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "远端切缘(DRM)", "relation": "标准要求", "tail": "标准要求: 肿瘤远端≥2cm；新辅助放化疗后或肿瘤位于直肠系膜边缘时，可缩小至≥1cm", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},

    # 手术技术
    {"head": "TME三大原则", "relation": "手术原则", "tail": "1.识别不同胚胎起源组织间的活动度；2.在良好光线下直视下锐性游离；3.通过持续牵引轻柔打开平面，避免撕扯", "source": "Heald B. TME technique description", "evidence": "专家共识", "domain": "外科手术"},
    {"head": "TME", "relation": "核心步骤", "tail": "步骤: 1.寻找系膜蒂包块；2.识别并打开神圣平面；3.后方游离；4.外侧游离至肛提肌水平；5.前方游离(按性别区分)；6.直肠切断与吻合", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME", "relation": "游离原则", "tail": "游离应保持在白色壁层筋膜与黄色脏层直肠系膜筋膜之间的蛛丝蜂窝组织潜在间隙中(神圣平面)", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME前方游离", "relation": "男性技术要点", "tail": "男性: 在腹膜反折褶前方切开腹膜，识别精囊腺，在精囊腺后方平面继续游离；大多数情况不切除Denonvilliers筋膜", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME前方游离", "relation": "女性技术要点", "tail": "女性: 从道格拉斯陷窝腹膜处开始，识别腹膜，锐性游离将阴道从直肠分离；吻合时特别注意将直肠与阴道牵开，避免阴道后壁被意外纳入", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME标本", "relation": "质量标准", "tail": "完整TME标本特征: 完整切除带有完整包膜筋膜的淋巴结承载直肠系膜，外观呈球状双叶形组织块，后方正中线有肛尾缝造成的凹陷", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME", "relation": "手术难度因素", "tail": "增加TME难度的因素: 高BMI、放疗后时间间隔、肿瘤位于前壁、肿瘤下缘与肛直肠交界距离短、肿瘤体积大、直肠系膜体积大、男性前列腺体积大", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "TME", "relation": "最困难区域", "tail": "直肠远端1/3的游离是TME中最困难的部分，是环周切缘完整性最大威胁的区域，也是局部复发率最高风险区", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},

    # 并发症
    {"head": "骶前大出血", "relation": "TME术中并发症", "tail": "骶前大出血是TME严重术中并发症，原因是破坏骶前筋膜前层面，暴露高压骶前静脉", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "TME术后并发症", "relation": "主要类型", "tail": "TME术后主要并发症: 吻合口漏、吻合口失败、泌尿功能障碍、性功能障碍(交感/副交感神经损伤)、局部复发", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "TME", "relation": "神经损伤预防", "tail": "交感神经损伤(尿失禁、逆行射精)多发生于IMA结扎或系膜游离时；副交感神经损伤(勃起困难、尿潴留)多发生于外侧或前方游离时", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},

    # 腹腔镜vs机器人vs taTME
    {"head": "腹腔镜TME", "relation": "局限性", "tail": "腹腔镜TME局限性: 器械铰接限制；窄骨盆中远端直肠锥形化风险；脐部摄像机难以观察精囊腺以下前方游离；转换率约10%", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "机器人TME", "relation": "技术优势", "tail": "机器人TME优势: 稳定的光学平台、器械可铰接、下骨盆可视性和操作性更好、遵循相同胚胎学手术平面", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "机器人TME", "relation": "技术局限", "tail": "机器人TME局限性: 吻合器最大角度<55°，低位垂直吻合困难；远端切缘判断不精确；设备投资和单例成本高", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "技术优势", "tail": "经肛TME(taTME)优势: 从肛门进行直肠远端1/3和系膜游离，可视性更好；远端切缘判断更精确；避免远端直肠不完美吻合", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "特殊风险", "tail": "taTME特殊风险: 男性尿道损伤风险(前列腺水平以下全层游离时)；需要验证过的培训路径和初期监督", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "最佳适应证", "tail": "taTME最佳适应证: 多种难度因素并存的低位直肠癌(如肥胖男性、窄骨盆、肿瘤体积大)", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "II级证据", "domain": "外科手术"},

    # 肿瘤学结局
    {"head": "TME", "relation": "历史疗效", "tail": "TME历史疗效: 早期经会阴切除术局部复发率近100%；Miles APR降至约30%；TME标准化后局部复发率大幅降低", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "病理·营养·预后"},
    {"head": "TME", "relation": "质量评估", "tail": "TME标本外观是手术质量的可靠预测指标，直肠系膜筋膜可作为手术切除质量的比较组织学标志", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "病理·营养·预后"},
    {"head": "MRI", "relation": "TME术前评估", "tail": "高分辨率骨盆T2加权MRI对显示直肠系膜筋膜、骶前筋膜平面、腹膜反折、Denonvilliers筋膜等关键解剖标志不可或缺，可用于直肠癌分期和手术规划", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "环周切缘(CRM)", "relation": "TME质量标志", "tail": "直肠远端1/3是威胁环周切缘(CRM)完整性最高风险的区域，手术质量主要由低位骨盆内的可操作性决定", "source": "Knol J, Keller DS. TME Technique. Clinics in Colon and Rectal Surgery. 2020", "evidence": "I级证据", "domain": "病理·营养·预后"},
]

# ========== 第二批：ERAS（术后加速康复）============

ERAS_TRIPLETS = [
    {"head": "ERAS协议", "relation": "定义", "tail": "ERAS(增强术后恢复)是一种多模式围手术期护理路径，旨在实现重大手术后的早期恢复，由多学科团队(外科、麻醉、护理、营养)实施", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "ERAS协议", "relation": "核心组成", "tail": "ERAS核心组成: 术前阶段(术前宣教、碳水化合物负荷、避免长时间禁食)；术中阶段(标准化麻醉、多模式镇痛)；术后阶段(早期活动、早期拔除导尿管、早期恢复口服进食)", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "住院时间", "tail": "Meta分析(17项研究): ERAS组住院时间平均缩短1.64天(95%CI: -2.21至-1.08, P<0.00001)", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "并发症减少", "tail": "Meta分析(18项研究): ERAS组术后并发症风险降低43%(OR=0.57, 95%CI: 0.46-0.71, P<0.00001)", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "再入院率", "tail": "Meta分析(9项研究): ERAS组30天再入院率降低43%(OR=0.57, 95%CI: 0.38-0.85, P=0.006)", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "胃肠功能恢复", "tail": "Meta分析: ERAS组首次排便时间平均提前0.74天、首次活动时间提前0.55天、首次经口进食时间提前0.62天", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "患者满意度", "tail": "Meta分析(12项研究): ERAS组患者满意度评分显著提高(MD=1.02, 95%CI: 0.19-1.86, P=0.02)", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "II级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "实施要点", "tail": "ERAS成功实施关键: 多学科协作、方案标准化、患者教育与参与、持续监测与反馈", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "结直肠手术ERAS", "relation": "长期生存", "tail": "部分研究表明: 接受ERAS协议的结直肠癌手术患者可能获得更好的总生存率，高依从性与更好的预后相关", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "II级证据", "domain": "病理·营养·预后"},
    {"head": "ERAS协议", "relation": "适用手术", "tail": "ERAS协议的有效性已在开放手术、腹腔镜手术和机器人手术等多种手术方式中得到证实", "source": "Turaga AH. ERAS Protocols for Colorectal Surgery. Cureus. 2023;15(7):e41755. PMC10416136", "evidence": "I级证据", "domain": "围手术期管理"},
]

# ========== 第三批：吻合口漏============

AL_TRIPLETS = [
    {"head": "吻合口漏", "relation": "定义与发生率", "tail": "吻合口漏(AL)是结直肠手术后严重并发症，发生率2%-19%，相关死亡率0.8%-27%，显著影响无病生存率、总生存率和局部复发率", "source": "Zarnescu EC et al. Updates of Risk Factors for Anastomotic Leakage after Colorectal Surgery. Diagnostics (Basel). 2021;11(12):2189. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "男性危险因素", "tail": "男性是吻合口漏的独立危险因素，所有类型结直肠吻合口中男性泄漏率均更高，Jannasch等报告男性泄漏发生率是女性的1.7倍", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "ASA评分", "tail": "ASA评分≥3是吻合口漏的独立危险因素，Charlson合并症指数(CCI)≥3患者泄漏风险是CCI=0患者的1.82倍", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "吸烟影响", "tail": "吸烟是吻合口漏危险因素(Kwak等报告OR=6.529)，机制: 尼古丁诱导血管收缩和微血栓形成，一氧化碳诱导细胞缺氧，抑制吻合口循环", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "肥胖影响", "tail": "BMI>30 kg/m²是吻合口漏独立危险因素；CT测量的内脏脂肪与吻合口漏和再手术直接相关；内脏肥胖增加并发症率和吻合口漏率", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "营养状态", "tail": "术前清蛋白水平<3.5 g/dL是重要危险因素；营养风险筛查阳性患者结直肠术后并发症率更高", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "病理·营养·预后"},
    {"head": "吻合口漏", "relation": "皮质类固醇", "tail": "长期使用皮质类固醇是吻合口漏危险因素；术前使用类固醇(用于肺部合并症)增加吻合口裂开风险，前瞻性研究已证实", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "吻合口位置", "tail": "距肛缘<5cm的低位吻合泄漏风险最高，比距肛缘>5cm高6.5倍；腹膜外吻合泄漏率4.7%，腹腔内吻合0.2%", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "腹腔镜vs开腹", "tail": "多项RCT和Meta分析显示: 腹腔镜与开腹手术的吻合口漏发生率无显著差异，COLOR II试验证实这一点", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "急诊手术", "tail": "急诊切除是吻合失败的独立危险因素；急诊手术+高ASA评分(3-5级)患者应考虑转流性造口或避免一期吻合", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "手术时间", "tail": "手术时间>3小时与吻合口漏风险增加相关；Midura等发现: 开放手术和手术时间>3小时与轻微和重大泄漏均相关", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "ICG血管造影", "tail": "近红外成像(NIR)使用吲哚菁绿(ICG)评估血供: 400例研究中11例(2.8%)因荧光异常需要改变切除线，AL率仅1%，有助于减少吻合口漏", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "II级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "保护性造口", "tail": "转流性造口不能减少吻合口漏发生率，但可减轻临床后果(有造口组5.8% vs 无造口组16.3%)；回肠造口优于结肠造口(并发症更少)", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "预防性引流", "tail": "腹膜外 colorectal 吻合术后预防性引流对吻合口漏发生率无影响(p=0.37)；可能延迟泄漏的诊断，建议直肠癌切除后不使用盆腔引流", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "围手术期输血", "tail": "术中失血和输血均增加吻合口漏风险: 输血患者风险增加1.5倍(机制: 免疫抑制，增加吻合口周围感染风险)", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "术后贫血", "tail": "术后血红蛋白<11 g/dL增加吻合口漏风险；机制: 组织氧输送能力下降，导致缺血风险增加", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "II级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "预防策略", "tail": "推荐的吻合口漏预防策略: 联合机械+口服抗生素肠道准备、术中使用ICG荧光血管造影、低位吻合时使用转流性造口、避免长时间手术", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "LARS与并发症"},
    {"head": "吻合口漏", "relation": "长期预后", "tail": "吻合口漏显著影响长期预后: 总生存率降低、无病生存率降低、局部复发率增加、永久性造口形成率增加；Meta分析(154,981例)证实对总生存率有负面影响", "source": "Zarnescu EC et al. Updates of Risk Factors for AL. Diagnostics (Basel). 2021. PMC8700187", "evidence": "I级证据", "domain": "病理·营养·预后"},
]

# ========== 第四批：机器人vs腹腔镜============

ROBOTIC_TRIPLETS = [
    {"head": "机器人辅助手术(RACS)", "relation": "定义", "tail": "机器人辅助结直肠癌手术(RACS)使用达芬奇手术系统，与传统腹腔镜手术(LACS)相比具有三维高清视野、7自由度仿生腕式机械臂、震颤过滤和运动缩放功能", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "视觉系统比较", "tail": "RACS提供高清三维(3D)放大视野；LACS为二维(2D)视野，腹腔镜TME时脐部摄像机难以观察精囊腺以下前方游离", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS", "relation": "操作优势", "tail": "RACS操作优势: 7自由度仿生腕式机械臂可完成更精细操作；具备震颤过滤和运动缩放功能；人体工程学设计更好，术者疲劳度更低", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "手术时间", "tail": "Meta分析(11项RCT, 1656 vs 1759例): RACS手术时间显著更长，平均比LACS多18-39分钟(P<0.00001)，部分源于机器人对接时间和学习曲线效应", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "术中出血", "tail": "Meta分析: RACS术中出血量显著更少，平均减少5.35-33.24mL (P=0.007)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "转开腹率", "tail": "Meta分析: RACS转开腹率显著更低，相对风险(RR)为0.40-0.76 (P=0.0003)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "并发症发生率", "tail": "Meta分析: RACS总体并发症发生率显著更低(RR=0.64-0.89, P=0.0009)；再次手术率也显著更低(RR=0.33-0.96, P=0.03)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "围手术期死亡率", "tail": "Meta分析: RACS与LACS围手术期死亡率无显著差异(RR=0.24-1.62, P=0.33)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS vs LACS", "relation": "住院时间", "tail": "Meta分析: RACS组住院时间显著更短，平均缩短0.33-1.60天(P=0.003)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "RACS vs LACS", "relation": "胃肠功能恢复", "tail": "Meta分析: RACS与LACS在首次排气时间(P=0.38)、首次自主排尿时间(P=0.11)、首次排便时间(P=0.15)、首次恢复饮食时间(P=0.08)均无显著差异", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "围手术期管理"},
    {"head": "RACS vs LACS", "relation": "肿瘤学质量", "tail": "Meta分析: RACS远端切缘显著更长(平均多0.04-0.94cm, P=0.03)；完整TME率显著更高(RR=1.01-1.08, P=0.006)；不完整TME率显著更低(RR=0.67-0.95, P=0.01)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "病理·营养·预后"},
    {"head": "RACS vs LACS", "relation": "淋巴结清扫", "tail": "Meta分析: RACS与LACS在清扫淋巴结数量上无显著差异(P=0.09)；环周切缘(CRM)阳性率也无显著差异(P=0.05，临界)", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "I级证据", "domain": "外科手术"},
    {"head": "RACS", "relation": "学习曲线", "tail": "RACS学习曲线: 右半结肠癌切除术中，术者完成21例机器人手术后，手术时间可与LACS持平；需完整学习课程和初期监督", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "机器人TME", "relation": "局限性", "tail": "机器人TME局限性: 吻合器最大角度<55°，低位垂直吻合困难；远端切缘判断不精确；设备投资和单例成本高", "source": "Frontiers in Oncology. Comparison of robotic-assisted vs laparoscopic colorectal surgery. 2023. PMC1273378", "evidence": "II级证据", "domain": "外科手术"},
]

# ========== 第五批：taTME============

TATME_TRIPLETS = [
    {"head": "taTME", "relation": "定义", "tail": "taTME(经肛全直肠系膜切除术)是一种从肛门进行直肠远端1/3和系膜游离的微创手术方式，用于治疗中下段直肠恶性肿瘤", "source": "Nature Scientific Reports. Transanal total mesorectal excision (TaTME) in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "适应证", "tail": "taTME主要适应证: 肿瘤距肛缘线50mm以内的低位直肠癌；50-100mm的中段直肠癌伴肥胖(BMI>35)、男性或狭窄骨盆等解剖困难因素", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "手术团队", "tail": "taTME需要两个手术团队同步操作: 腹部团队(建立气腹、游离脾曲、处理血管)和经肛团队(从肛门建立通道、游离直肠远端)", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "经肛步骤", "tail": "taTME经肛步骤: 使用GelPort系统经肛建立通道→肿瘤下方10mm处荷包缝合关闭直肠腔→冲洗消毒→环形切开直肠→向近端游离系膜至腹膜返折→两手术野汇合", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "吻合方式", "tail": "taTME吻合: 确认血供(ICG)→荷包缝合近端结肠和直肠残端→圆形吻合器(29-31mm)完成端端结肠肛管吻合→检查吻合口渗漏", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "手术结局", "tail": "taTME手术结局(128例): 成功率99.22%；平均手术时间169分钟(110-260分钟)；平均失血量200mL(100-550mL)；平均住院7.26天(4-48天)", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "并发症", "tail": "taTME并发症(127例): 总发生率17.32%；吻合口漏7.87%(10例，5例内镜负压治疗，5例Hartmann术)；回肠造口狭窄3.15%；手术部位感染1.58%；尿道损伤0.79%", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "LARS与并发症"},
    {"head": "taTME", "relation": "R0切除率", "tail": "taTME R0切除率达98.43%(125/127例)；近端和远端切缘全部阴性；2例R1切除(环周切缘<1mm)均来自T4期患者", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "病理·营养·预后"},
    {"head": "taTME", "relation": "长期结局", "tail": "taTME长期结局(平均随访795天): 局部复发率1.57%(2例)；远处转移率4.72%(6例)；死亡4例(均为广泛转移患者)", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "病理·营养·预后"},
    {"head": "taTME", "relation": "技术优势", "tail": "taTME优势: 低位直肠肿瘤可视化更好；远端切缘判定更准确；更彻底的盆腔深部解剖；在男性或肥胖患者中优势更明显；保留肛门括约肌功能", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "学习曲线", "tail": "taTME学习曲线陡峭，需约40-50例的经验积累；需要两个经验丰富的手术团队；建议在年手术量大的专业中心开展", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "特殊风险", "tail": "taTME特殊风险: 2020年挪威研究报告了较高的并发症和局部复发率，该技术在挪威曾被暂停实施；提示需要标准化培训体系和质量控制", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "LARS与并发症"},
    {"head": "taTME", "relation": "保护性造口", "tail": "taTME建议常规建立保护性回肠造口(该研究中62.99%患者建立)；回肠造口在6-8周后还纳", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "外科手术"},
    {"head": "taTME", "relation": "术后管理", "tail": "taTME术后管理: 持续镇痛→术后第1天开始活动后拔除Redon引流管→术后第1天恢复口服进食→无并发症患者术后第3天出院", "source": "Nature Scientific Reports. TaTME in rectal cancer. 2023. PMC4424788", "evidence": "II级证据", "domain": "围手术期管理"},
]

# ========== 合并入库 ==========

def merge_into_kb(new_triplets, kb_path):
    """将新三元组合并到主知识库"""
    with open(kb_path, 'r', encoding='utf-8') as f:
        kb = json.load(f)

    print(f"当前知识库: {len(kb)} 条")

    # 去重
    seen = set()
    unique = []
    for t in kb:
        key = (t.get('head',''), t.get('relation',''), t.get('tail','')[:60])
        seen.add(key)
        unique.append(t)

    added = 0
    for t in new_triplets:
        key = (t.get('head',''), t.get('relation',''), t.get('tail','')[:60])
        if key not in seen and len(t.get('tail','')) >= 15:
            seen.add(key)
            unique.append(t)
            added += 1

    print(f"新增: {added} 条，总计: {len(unique)} 条")

    with open(kb_path, 'w', encoding='utf-8') as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

    return unique, added

# 运行
all_new = TME_TRIPLETS + ERAS_TRIPLETS + AL_TRIPLETS + ROBOTIC_TRIPLETS + TATME_TRIPLETS
print(f"准备入库: {len(all_new)} 条")
print(f"  TME: {len(TME_TRIPLETS)} 条")
print(f"  ERAS: {len(ERAS_TRIPLETS)} 条")
print(f"  吻合口漏: {len(AL_TRIPLETS)} 条")
print(f"  机器人: {len(ROBOTIC_TRIPLETS)} 条")
print(f"  taTME: {len(TATME_TRIPLETS)} 条")

kb_final, added = merge_into_kb(all_new, KB_PATH)

# 统计
from collections import Counter
domains = Counter(t.get('domain','未知') for t in kb_final)
sources = Counter(t.get('source','') for t in kb_final)

print(f"\n最终知识库: {len(kb_final)} 条")
print(f"新增: {added} 条")
print("\n知识域分布(前10):")
for d, cnt in sorted(domains.items(), key=lambda x:-x[1])[:10]:
    print(f"  {d}: {cnt}")
print(f"\n知识来源: {len(sources)} 个")
