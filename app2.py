import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import matplotlib.font_manager as fm
import pandas as pd


merge_final = pd.read_excel("0917대학역량측면데이터.xlsx")


# -----------------------------
# 폰트 설정
# -----------------------------
font_path = "KoPubWorld Dotum Medium.ttf"  # 앱과 같은 폴더에 폰트 넣어두기
font_path2 = "KoPubWorld Dotum Bold.ttf"
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# --- 라벨용 FontProperties (사이즈 포함) ---
font_prop_labels_for_label = fm.FontProperties(fname=font_path, size=13, weight = 'bold')
font_prop_labels_for_legend = fm.FontProperties(fname=font_path, size=11, weight = 'bold')
font_prop_labels_for_box = fm.FontProperties(fname=font_path, size=9, weight = 'bold')
font_prop_labels_for_box_title = fm.FontProperties(fname=font_path2, size=14, weight = 'bold')

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(layout="wide")
st.title("대학 역량 측면")

school_name = st.selectbox("대학 선택", merge_final["학교"].unique(), index=0)

# -----------------------------
# 데이터 준비
# -----------------------------
areas = ["교육", "연구", "산학창업", "글로벌"]
row = merge_final[merge_final["학교"] == school_name].iloc[0]
school_vals = [float(row[a + "_평균"]) for a in areas]

region = row["지역"]
region_vals = merge_final[merge_final["지역"] == region][[a + "_평균" for a in areas]].mean().values.tolist()
national_vals = merge_final[[a + "_평균" for a in areas]].mean().values.tolist()

# -----------------------------
# Figure 생성
# -----------------------------
fig = plt.figure(figsize=(11, 9))
fig.patch.set_facecolor("#BFBFBF")

ax = fig.add_axes([0.18, 0.12, 0.64, 0.76])
ax.set_facecolor("#F2F2F2")
ax.axis("equal")
ax.axis("off")

# -----------------------------
# 사각형 레이더 좌표 변환
# -----------------------------
def to_square_coords(vals, vmin, vmax):
    norm = [(v - vmin) / (vmax - vmin) for v in vals]
    pts = [(0, norm[0]), (norm[1], 0), (0, -norm[2]), (-norm[3], 0)]
    return np.array(pts + [pts[0]])

stack = np.array(school_vals + region_vals + national_vals)
lo, hi = np.min(stack), np.max(stack)
pad = max((hi - lo) * 0.35, 0.12)
vmin, vmax = lo - pad, hi + pad

school_xy = to_square_coords(school_vals, vmin, vmax)
region_xy = to_square_coords(region_vals, vmin, vmax)
national_xy = to_square_coords([5]*4, vmin, vmax)

# -----------------------------
# 배경 원 & 격자
# -----------------------------
circle = plt.Circle((0,0), 1.25, transform=ax.transData,
                    facecolor="#E5E5E5", edgecolor="none", alpha=0.6, zorder=0)
ax.add_patch(circle)

for r in np.linspace(0.2, 1, 5):
    poly = Polygon([(0,r),(r,0),(0,-r),(-r,0)], closed=True,
                   facecolor="white", edgecolor="#DDDDDD", linewidth=0.7, alpha=0.6)
    ax.add_patch(poly)

# 축 라벨
ax.text(0,1.1,"교육",ha="center",va="bottom",fontproperties=font_prop_labels_for_label)
ax.text(1.1,0,"연구",ha="left",va="center",fontproperties=font_prop_labels_for_label)
ax.text(0,-1.1,"창업 및 산학협력",ha="center",va="top",fontproperties=font_prop_labels_for_label)
ax.text(-1.1,0,"국제화",ha="right",va="center",fontproperties=font_prop_labels_for_label)

# -----------------------------
# 데이터 플롯
# -----------------------------
ax.plot(school_xy[:,0], school_xy[:,1], linewidth=2.6, color="#E3342F", label=school_name)
ax.plot(region_xy[:,0], region_xy[:,1], linewidth=2.3, color="#000000", label=f"{region} 평균")
ax.plot(national_xy[:,0], national_xy[:,1], linewidth=2.0, color="#B0B0B0", label="전국 평균")

for (x,y), val in zip(school_xy[:-1], school_vals):
    ax.text(x*1.15, y*1.15, f"{val:.2f}", ha="center", va="center",
            fontsize=12, fontweight="bold", color="#E3342F")

ax.legend(loc="lower left", bbox_to_anchor=(-0.0,0.35),
          ncol=1, frameon=False, prop=font_prop_labels_for_legend)

# -----------------------------
# 네모 설명 박스 (Streamlit 대응)
# -----------------------------
def draw_info_box(ax, x, y, w, h, title, content):
    body = patches.Rectangle((x,y), w, h,
                             transform=ax.transAxes,
                             facecolor="#E6E6E6", edgecolor="gray", zorder=2)
    ax.add_patch(body)

    header_h = 0.05
    header = patches.Rectangle((x,y+h-header_h), w, header_h,
                               transform=ax.transAxes,
                               facecolor="black", edgecolor="black", zorder=3)
    ax.add_patch(header)

    ax.text(x+w/2, y+h-header_h/2, title,
            ha="center", va="center", color="white", fontproperties=font_prop_labels_for_box_title, zorder=4,
            transform=ax.transAxes)
    ax.text(x+0.01, y+h-header_h-0.01, content,
            ha="left", va="top", color="black", fontproperties=font_prop_labels_for_box, zorder=4,
            transform=ax.transAxes)

# 박스 4개
draw_info_box(ax, 0.02, 0.72, 0.35, 0.25, "I. 교육분야",
              "• 신입생 충원율, 신입생 경쟁률\n• 재학생충원율\n• 중도탈락률\n• 전임교원확보율(정원내)\n• 전임교원강의비율\n• 학생1인당 교육비\n• 재학생1인당 장학금\n• 등록금\n• 취업률, 유지취업률")
draw_info_box(ax, 0.63, 0.72, 0.35, 0.25, "II. 연구분야",
              "\n\n• 전임교원 1인당 연구 실적 교내\n• 전임교원 1인당 연구 실적 교외\n• 전임교원 1인당 연구비 교내\n• 전임교원 1인당 연구비 교외\n• 졸업생 진학률")
draw_info_box(ax, 0.02, 0.05, 0.35, 0.25, "IV. 국제화분야",
              "\n\n\n• 학생1인당 외국인 전임교원 수\n• 외국인 학생수\n• 외국인 중도 탈락률")
draw_info_box(ax, 0.63, 0.05, 0.35, 0.25, "III. 창업 및 산학협력",
              "\n• 산업체경력전임교원수\n• 기술이전 수입료\n• 현장실습이수학생 수\n• 캡스톤디자인 이수학생 수\n• 학생창업자 수\n• 교원창업자 수\n• 학생창업 지원액")

# -----------------------------
# Streamlit에 출력
# -----------------------------
st.pyplot(fig)