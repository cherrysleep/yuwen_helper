import streamlit as st
from openai import OpenAI

# ========== 素材库（共30+条，覆盖10+论点） ==========
data = [
    # 坚持
    ("坚持", "锲而不舍，金石可镂", "爱迪生试验上千次发明电灯", "荀子《劝学》"),
    ("坚持", "只要功夫深，铁杵磨成针", "李白受老媪启发坚持学习", "谚语"),
    ("坚持", "滴水穿石非一日之功", "王羲之临池学书染黑池水", "《汉书》"),
    # 创新
    ("创新", "苟日新，日日新，又日新", "蔡伦改进造纸术", "《大学》"),
    ("创新", "创新是民族进步的灵魂", "袁隆平杂交水稻创新突破", "俗语"),
    ("创新", "穷则变，变则通，通则久", "商鞅变法推动时代进步", "《周易》"),
    # 诚信
    ("诚信", "人无信不立", "商鞅立木为信", "孔子"),
    ("诚信", "言必信，行必果", "季布一诺千金", "《论语》"),
    ("诚信", "诚信为人之本", "宋濂守信抄书还书", "鲁迅"),
    # 奋斗
    ("奋斗", "奋斗是青春最亮丽的底色", "苏炳添刻苦训练突破极限", "俗语"),
    ("奋斗", "天道酬勤", "匡衡凿壁偷光刻苦求学", "《周易》"),
    ("奋斗", "以奋斗铸就辉煌", "钱学森归国艰苦奋斗研导弹", "俗语"),
    # 责任
    ("责任", "天下兴亡，匹夫有责", "林则徐虎门销烟担家国责任", "顾炎武"),
    ("责任", "士不可以不弘毅", "焦裕禄扎根兰考担为民责任", "曾子"),
    ("责任", "责任重于泰山", "抗疫医护坚守岗位护生命", "俗语"),
    # 挫折
    ("挫折", "宝剑锋从磨砺出", "司马迁受宫刑著《史记》", "谚语"),
    ("挫折", "千磨万击还坚劲", "贝多芬失聪创作交响曲", "郑板桥"),
    ("挫折", "逆境是最好的学校", "霍金身患重病探索宇宙", "俗语"),
    # 合作
    ("合作", "众人拾柴火焰高", "蚂蚁合作搬运食物", "谚语"),
    ("合作", "天时不如地利，地利不如人和", "国共合作抗日卫国", "孟子"),
    ("合作", "三个臭皮匠，顶个诸葛亮", "中国女排夺冠靠团队配合", "谚语"),
    # 梦想
    ("梦想", "志当存高远", "马云创建阿里巴巴", "诸葛亮"),
    ("梦想", "心有多大，舞台就有多大", "袁隆平禾下乘凉梦", "俗语"),
    ("梦想", "不忘初心，方得始终", "乔布斯重返苹果", "《华严经》"),
    # 谦虚
    ("谦虚", "满招损，谦受益", "梅兰芳拜师学艺", "《尚书》"),
    ("谦虚", "三人行必有我师", "孔子问礼于老子", "《论语》"),
    ("谦虚", "虚心使人进步", "牛顿说自己站在巨人肩上", "毛泽东"),
    # 勇气
    ("勇气", "不入虎穴，焉得虎子", "钟南山逆行抗疫", "《后汉书》"),
    ("勇气", "狭路相逢勇者胜", "刘翔跨栏夺冠", "俗语"),
    ("勇气", "敢于向黑暗宣战", "鲁迅弃医从文", "俗语"),
    # 感恩
    ("感恩", "滴水之恩当涌泉相报", "韩信报漂母一饭之恩", "俗语"),
    ("感恩", "谁言寸草心，报得三春晖", "黄香温席", "孟郊"),
    ("感恩", "吃水不忘挖井人", "乡亲感恩毛主席", "俗语"),
    # 时间
    ("时间", "一寸光阴一寸金", "鲁迅把时间当海绵", "俗语"),
    ("时间", "少壮不努力，老大徒伤悲", "王献之练字", "《长歌行》"),
    ("时间", "逝者如斯夫，不舍昼夜", "珍惜时间的毛泽东", "孔子"),
    # 爱国
    ("爱国", "天下兴亡，匹夫有责", "钱学森回国", "顾炎武"),
    ("爱国", "先天下之忧而忧", "范仲淹戍边", "范仲淹"),
    ("爱国", "为中华之崛起而读书", "周恩来少年立志", "周恩来"),
    # 读书
    ("读书", "书中自有黄金屋", "匡衡凿壁偷光", "宋真宗"),
    ("读书", "读万卷书，行万里路", "李白游历", "俗语"),
    ("读书", "读书破万卷，下笔如有神", "杜甫", "杜甫"),
]

# ========== 页面配置 ==========
st.set_page_config(page_title="议论文素材宝", page_icon="📝")
st.title("📝 AI高中议论文论点-素材匹配系统")
st.caption("真实素材库 + AI段落生成 | 不编造，可溯源")

# ========== 侧边栏：素材统计 ==========
with st.sidebar:
    st.subheader("📚 素材库统计")
    topics_list = list(set([t[0] for t in data]))
    st.write(f"✅ 共 {len(data)} 条真实素材")
    st.write(f"✅ 覆盖 {len(topics_list)} 种论点类型")
    st.write("**论点类型：**")
    for t in sorted(topics_list):
        st.write(f"- {t}")

# ========== 选择模型 ==========
st.subheader("🤖 选择AI模型")
model_choice = st.radio(
    "模型选择",
    ["通义千问（百炼，免费）", "DeepSeek（已充值）"],
    horizontal=True,
    label_visibility="collapsed"
)

# ========== 选择论点 ==========
col1, col2 = st.columns([1, 2])

with col1:
    selected_topic = st.selectbox("📌 选择论点", sorted(topics_list))

with col2:
    st.write("")
    st.write("")
    st.write(f"当前论点：**{selected_topic}**")

# ========== 匹配素材 ==========
matched = [t for t in data if t[0] == selected_topic]

if matched:
    st.subheader("📖 匹配到的素材")

    # 如果有多个素材，让用户选择用哪个
    if len(matched) > 1:
        selected_idx = st.radio(
            "选择要使用的素材",
            range(len(matched)),
            format_func=lambda i: f"{matched[i][1]} —— {matched[i][2][:20]}...",
            horizontal=True
        )
        selected = matched[selected_idx]
    else:
        selected = matched[0]

    # 显示选中的素材
    st.info(f"**名言：** {selected[1]}")
    st.info(f"**事例：** {selected[2]}")
    st.info(f"**出处：** {selected[3]}")
else:
    st.warning("暂无匹配素材")
    st.stop()

# ========== API Key 输入 ==========
st.subheader("🔑 API 配置")

if model_choice == "通义千问（百炼，免费）":
    api_key = st.text_input(
        "通义千问 API Key（sk-开头）",
        type="password",
        help="去 https://bailian.console.aliyun.com 获取"
    )
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    model_name = "qwen-turbo"
else:
    api_key = st.text_input(
        "DeepSeek API Key（sk-开头）",
        type="password",
        help="去 https://platform.deepseek.com 获取"
    )
    base_url = "https://api.deepseek.com"
    model_name = "deepseek-chat"

# ========== 生成按钮和Prompt ==========
prompt = f"""你是高中议论文写作助手。请严格按照以下结构写一段标准议论文段落：

1. 观点句（一句话点题，1句）
2. 引用素材（先写名言，再写事例，2-3句）
3. 道理分析（分析为什么这个素材能证明观点，2-3句）
4. 回扣论点（一句话总结，1句）

论点：{selected_topic}
名言：{selected[1]}
事例：{selected[2]}
出处：{selected[3]}

要求：
- 语言正式、客观，符合高考作文规范
- 不编造任何内容
- 段落完整，150-200字左右
- 逻辑连贯，层层递进"""

if st.button("🚀 生成议论文段落", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ 请输入API Key")
    else:
        with st.spinner("AI正在生成中..."):
            try:
                client = OpenAI(api_key=api_key, base_url=base_url)
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                st.success("✅ 生成成功！")
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                st.markdown("---")
                st.caption(f"🤖 生成模型：{model_choice} | 📚 素材来源：{selected[3]}")
            except Exception as e:
                st.error(f"❌ 出错：{e}")
                st.info("💡 提示：请检查API Key是否正确，或网络是否正常")

# ========== 页脚 ==========
st.divider()
st.caption("📝 议论文素材宝 | 真实素材库 + AI智能生成 | 专为高中生议论文写作设计")