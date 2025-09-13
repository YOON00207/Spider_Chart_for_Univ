import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
import matplotlib.patheffects as path_effects
import pandas as pd

#파일 불러오기
df_result = pd.read_excel("09118페이지1번Z점수화필터링후.xlsx")

# -----------------------------
# 한글 폰트 설정
# -----------------------------
font_path = r"C:\Users\윤서현\Downloads\KoPubWorld Dotum_Pro Medium.otf"
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("9-1 대학운영측면")
school_name = st.text_input("대학명을 입력하세요", "국립강릉원주대학교")

if school_name in df_result["학교"].values:
    row = df_result[df_result["학교"] == school_name].iloc[0]
    school_region = row["지역"]
    school_estab = row["설립구분"]

    # 지표 순서
    custom_order = ["신입생 충원율", "신입생 경쟁률", "외국인 학생수",  "재학생 충원율",
                    "중도탈락률", "전임교원강의비율", "전임교원확보율", "장학금", "취업률", 
                    "1인당 교육비", "등록금", "교원연구(국내)",
                    "교원연구(SCI)", "교원연구(저역서)"]

    labels = custom_order
    num_vars = len(labels)

    # 데이터 준비
    school_scores = row[[f"{col}_전국Z" for col in custom_order]].values
    region_scores = row[[f"{col}_전국Z_지역평균" for col in custom_order]].values
    estab_scores = row[[f"{col}_전국Z_설립평균" for col in custom_order]].values
    region_estab_scores = row[[f"{col}_전국Z_지역설립평균" for col in custom_order]].values
    nation_scores = np.array([5] * num_vars)

    scores_list = [
    nation_scores,
    region_scores,
    estab_scores,
    school_scores,
    region_estab_scores
]

    labels_list = [ "전국평균",
                   f"{school_region} 평균",
                   f"{school_estab} 평균",
                   school_name, 
                f"{school_region}+{school_estab} 평균"]


    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # -----------------------------
    # 레이더 차트 그리기
    # -----------------------------
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))

    colors = {
    school_name : "#B22222",        # 빨강
    f"{school_region} 평균": "#000080",    # 남색
    f"{school_estab} 평균": "#D3D3D3",    # 밝은회색
    f"{school_region}+{school_estab} 평균": "#ADD8E6", # 연한파랑
    "전국평균": "#000000"     # 검정
}
    for scores, lab in zip(scores_list, labels_list):
        values = np.concatenate((scores, [scores[0]]))
        angle_vals = np.concatenate((angles, [angles[0]]))
    
        if lab == school_name:  # 선택 대학만 색 채우기 + 더 굵은 선
            ax.plot(angle_vals, values, label=lab, color=colors[lab], linewidth=3.5)
            ax.fill(angle_vals, values, alpha=0.25, color=colors[lab])
        else:  # 나머지는 선만
            ax.plot(angle_vals, values, label=lab, color=colors[lab], linewidth=3.5)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=13, weight="bold")
    
    ax.set_theta_offset(np.pi / 2)  # 90도 회전
    ax.set_theta_direction(-1) #반시계
    ax.set_ylim(3.1, 6.4) #y축 변경

    ax.set_yticks([4, 5, 6])
    ax.set_yticklabels(["4", "5", "6"], fontsize=10, color="gray")
    ax.set_facecolor("white")

    # 원형(동심원)만 남기기
    ax.xaxis.grid(False)  # 세로선 제거
    ax.yaxis.grid(True, linestyle="--", color="lightgray", alpha=0.7)
    ax.spines['polar'].set_color("lightgray")
    ax.spines['polar'].set_linestyle("--")

    # 대학 점수값 표시
    for angle, score in zip(angles, school_scores):
        txt = ax.text(angle, score + 0.25, f"{score:.2f}",
                  ha="center", va="center",
                  fontsize=15, color="#B22222", weight="bold")
        txt.set_path_effects([path_effects.Stroke(linewidth=2, foreground="white"),
                          path_effects.Normal()])
    # 범례
    ax.legend(
    loc="upper center", 
    bbox_to_anchor=(0.5, 1.15),
    ncols = 5,
    fontsize = 12,
    markerscale = 2.0,
    title=None,     # 범례 제목 제거
    frameon=False   # (선택) 범례 박스 테두리 제거
)

    # -----------------------------
    # Streamlit에 출력
    # -----------------------------
    st.pyplot(fig)

else:
    st.warning("대학명을 정확히 입력해주세요")