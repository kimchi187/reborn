# -*- coding: utf-8 -*-
"""
重启计划 · 情绪支持小工具（Streamlit 版本）

使用方法：
1. python3 -m pip install streamlit
2. 把本文件命名为 app.py
3. 在终端运行：python3 -m streamlit run app.py
4. 浏览器会自动打开一个网页
"""

import streamlit as st
from datetime import datetime
import os

# 本地日记文件名
JOURNAL_FILE = "journal_entries.txt"


def init_state():
    """初始化会话状态"""
    if "mood_history" not in st.session_state:
        st.session_state["mood_history"] = []


# ================== 各个页面 ================== #

def page_home():
    st.title("重启计划 · 情绪支持 Demo")

    st.markdown(
        """
        欢迎来到 **重启计划**。  
        这是一个本地运行的小工具，用**温和、不评判**的方式，
        帮你在情绪低谷的时候，多一点支撑。

        你可以在这里：

        - **情绪签到**：记录今天的心情，看看自己这段时间的状态变化  
        - **自助练习**：尝试呼吸放松、地面化（专注当下）、自我安慰的练习  
        - **心情日记**：把卡在心里的话写出来，保存到本地文件（只有你自己能看到）  
        - **求助指南**：当你觉得扛不住时，提醒自己可以去找哪些支持  

        无论你现在状态如何，走到这里已经是一种  
        **“还在努力活着”** 的表现。
        """
    )


def page_checkin():
    init_state()

    st.header("情绪签到")
    st.write("给今天的整体心情打一个分数（0 = 极度痛苦，10 = 状态很好）。")

    mood = st.slider("今天的心情（0～10）", 0, 10, 5)
    note = st.text_area(
        "有什么想多说一点的吗？（可选）",
        placeholder="比如：为什么今天会这样？发生了什么事？"
    )

    if st.button("保存签到"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        st.session_state["mood_history"].append(
            {"time": now, "mood": mood, "note": note.strip()}
        )

        # 简单反馈
        if mood <= 3:
            st.warning(
                "今天好像真的挺难熬的。\n\n"
                "如果这种状态持续很多天，或者已经影响到睡眠、吃饭、上学/工作，"
                "可以考虑认真地找一个专业的人聊聊。"
            )
        elif mood <= 6:
            st.info(
                "今天可能一般般，也有点难受。\n\n"
                "可以写写日记、做几次呼吸练习，给自己一点缓冲空间。"
            )
        else:
            st.success(
                "不错，今天状态还可以。\n\n"
                "可以记一下：是什么让你稍微好一点？"
                "以后难受的时候，也许能再次用上这些东西。"
            )

        st.success("✅ 情绪签到已保存（本次运行内有效）。")

    # 最近记录
    if st.session_state["mood_history"]:
        st.subheader("最近的签到（最多显示 10 条）")
        for item in reversed(st.session_state["mood_history"][-10:]):
            line = f"{item['time']} · 心情 {item['mood']}/10"
            if item["note"]:
                line += f" · 备注：{item['note']}"
            st.write("• " + line)
    else:
        st.caption("还没有任何签到记录。可以先试着打一个分数～")


def page_exercises():
    st.header("自助练习")
    st.write("这里有几种简单、风险很低的自助练习，你可以慢慢尝试：")

    st.subheader("1️⃣ 60 秒呼吸放松")
    st.markdown(
        """
        - 找一个相对安静的地方，坐下或躺下都可以  
        - 用鼻子慢慢吸气，心里数「1、2、3、4」  
        - 屏住一小会儿（1～2 秒就行）  
        - 用嘴慢慢呼气，心里数「1、2、3、4、5、6」  
        - 重复 10 轮，如果中途不想继续也没关系  

        重点不是「做得多标准」，而是：  
        **给身体一个机会慢下来**。
        """
    )

    st.subheader("2️⃣ 5-4-3-2-1 地面化练习（专注当下）")
    st.markdown(
        """
        当你感到特别烦躁、恐慌、心里很乱时，可以试试：

        - **看一看**：说出你能看到的 **5** 样东西  
        - **摸一摸**：感受你能触碰到的 **4** 样东西（衣服、椅子、手机…）  
        - **听一听**：注意你能听到的 **3** 种声音  
        - **闻一闻**：找 **2** 种味道（空气、饮料、环境的味道）  
        - **想一想**：此刻你还感到感激的 **1** 件小事  

        目的：把你从「一直在脑子里打转」轻轻拉回到**此时此刻**。
        """
    )

    st.subheader("3️⃣ 自我安慰话术模板")
    st.markdown(
        """
        你可以在心里，或者写在日记里，对自己说一些话，例如：

        > 「我现在真的挺难受，这种感觉是**真实的**，也值得被认真对待。」  
        > 「也许现在我想不起什么希望，但并不代表未来永远都这样。」  
        > 「哪怕我现在只能做到勉强撑着，那也是一种努力。」  

        把最有感觉的几句记下来，  
        在情绪很糟的时候拿出来看看。
        """
    )

    st.caption("💡 不用追求“做得完美”，能做到一点点就已经很不容易。")


def page_journal():
    st.header("心情日记")
    st.write("把卡在心里的话写出来，可以是碎片、抱怨、回忆，随便写。")

    text = st.text_area(
        "想写点什么？（只有你自己能看到，会保存到本地 journal_entries.txt）",
        height=220,
    )

    if st.button("保存日记到本地文件"):
        if text.strip():
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = f"=== {now} ===\n{text.strip()}\n\n"
            try:
                with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
                    f.write(entry)
                st.success("✅ 日记已保存到 journal_entries.txt（保存在当前运行目录）。")
            except Exception as e:
                st.error(f"保存失败：{e}")
        else:
            st.warning("可以先随便写一点，再保存也行。")

    # 显示最近日记结尾
    if os.path.exists(JOURNAL_FILE):
        try:
            with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                snippet = content[-800:]
                st.subheader("最近的一些日记片段：")
                st.text(snippet)
        except Exception:
            st.caption("日记文件存在，但暂时无法读取。")


def page_help():
    st.header("求助指南（非常重要）")

    st.markdown(
        """
        如果你已经被这些情绪影响到：

        - 持续几周以上的严重低落、绝望、对什么都没兴趣  
        - 睡眠、食欲明显改变（完全睡不着 / 一直想睡 / 吃不下或暴饮暴食）  
        - 经常出现「我活着有什么意义」「要不就这样算了」之类的念头  
        - 已经有了比较具体的自伤、自杀计划  

        那么 **非常建议** 你考虑寻求更专业的帮助，而不是一个人硬扛。
        """
    )

    st.subheader("1️⃣ 能做的专业求助方向")
    st.markdown(
        """
        - 去当地的 **医院精神科 / 心理门诊** 挂号  
        - 寻找 **持证心理咨询师 / 心理治疗师** 做系统的心理咨询  
        - 如果你在上学，可以找 **学校的心理咨询中心 / 学生支持服务**  
        """
    )

    st.subheader("2️⃣ 如果已经有强烈的自杀冲动")
    st.markdown(
        """
        这部分要非常认真对待，可以考虑：

        - 立即联系当地急救电话 / 紧急求助电话  
        - 拨打所在地区的心理危机干预 / 自杀干预热线  
        - 请信得过的家人 / 朋友陪同，直接去医院急诊  

        ⚠️ **不要一个人默默扛着。**  
        这不是“矫情”，而是一个真正需要治疗的健康问题。
        """
    )

    st.subheader("3️⃣ 给还在犹豫要不要求助的你")
    st.markdown(
        """
        很多人会想：

        > 「我是不是太矫情？」  
        > 「是不是没严重到要去看医生？」  

        一个简单标准是：  

        > 只要你已经被这些情绪影响到**正常生活和基本功能**  
        > （上学、工作、睡觉、吃饭、人际关系），  
        > 就完全有资格去求助。

        去看医生或者做心理咨询，不代表你“失败了”，  
        只代表你在为自己负责。
        """
    )


# ================== 主入口 ================== #

def main():
    st.set_page_config(
        page_title="重启计划 Demo",
        page_icon="🌱",
        layout="centered"
    )

    st.sidebar.title("重启计划 · 导航")
    page = st.sidebar.radio(
        "想去哪里看看：",
        ("首页", "情绪签到", "自助练习", "心情日记", "求助指南"),
    )

    st.sidebar.markdown(
        """
        ---
        💡 小提示：  
        这个工具只是一个**自助小辅助**，  
        **不能替代专业医疗或心理咨询**。  

        如果你有持续的自杀念头、已经拟好计划，  
        或者觉得自己随时可能做出危险行为，  
        **请立刻联系当地急救电话或危机干预热线。**
        """
    )

    if page == "首页":
        page_home()
    elif page == "情绪签到":
        page_checkin()
    elif page == "自助练习":
        page_exercises()
    elif page == "心情日记":
        page_journal()
    elif page == "求助指南":
        page_help()


if __name__ == "__main__":
    main()
