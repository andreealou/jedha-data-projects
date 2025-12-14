# P1 – Exploratory Data Analysis: Tinder Dataset

# 💘 Speed Dating Analysis – What Makes People Interested in Each Other?

## 🎯 Project Objective
This project was inspired by a Tinder business question:  
> **"What makes people interested in each other?"**

Using real **Speed Dating data** from 551 participants and 8,378 dates, we analyzed which factors influence the decision to go on a second date.

---

## 📊 Dataset Overview
- **Source:** Speed Dating Experiment dataset (open source)
- **Participants:** 551 individuals (men and women)
- **Total dates:** 8,378  
- **Format:** CSV file with 195 columns  
- **Key variables:**
  - `dec`: Decision to see the person again (0 = No, 1 = Yes)
  - `match`: Match indicator (1 if both said “Yes”)
  - `attr_o`, `sinc_o`, `intel_o`, `fun_o`, `amb_o`, `shar_o`: Ratings received for attractiveness, sincerity, intelligence, fun, ambition, and shared interests.
  - `age`, `field_cd`, `race`, `income`, `imprelig`: Demographics
  - `goal`, `go_out`, `date`: Lifestyle and dating behavior
  - `exphappy`: Expected happiness with people met during the event
  - `match_es`: Estimated number of matches by the participant

---

## 🧹 Data Preprocessing
The dataset required significant cleaning before analysis:
- Normalized all rating scales to 1–10.
- Handled missing values (kept them for transparency in analysis).
- Verified consistency across multiple time points (`_1`, `_2`, `_3` suffixes).
- Checked for and corrected out-of-range values.

---

## 📈 Exploratory Analysis

### 1. Participation and Missing Data
- **98.7%** of participants answered the pre-event questionnaire.  
- Only **65%** completed the next-day follow-up and **35%** the 3-weeks-later survey.  
→ Later responses were excluded from key comparisons due to high missingness.

### 2. Participants Overview
- **Age range:** Mostly between **22 and 31 years old.**
- **Goals:** Only ~11% came looking for a serious relationship or a date.
- **Gender:** Men say "yes" **10% more often** than women.

### 3. What Does *Not* Matter
No significant correlation was found between the decision (`dec`) and:
- Race  
- Religion  
- Income  
- Age difference  
- Field of study  
- Order of the date  
→ These factors **do not significantly affect** the “Yes” decision.

### 4. Shared Interests
The variable `int_corr` (interest correlation between partners) showed a **very weak positive link** with matches — shared interests **slightly help**, but they are not decisive.

### 5. Personality and Perception
Correlations between partner ratings and “Yes” decisions:
| Attribute | Correlation with Decision |
|------------|----------------------------|
| Intelligence | 0.082 |
| Sincerity | 0.081 |
| Ambition | 0.063 |
| Shared Interests | 0.058 |
| Fun | 0.044 |
| Attractiveness | -0.059 |

→ Intelligence and sincerity stand out slightly, but none are strong predictors.

### 6. Expected Happiness
The **strongest observed link** was between `exphappy` (expected happiness) and decision:
- Participants expecting to be happier were **more likely to say “yes.”**

---

## 💡 Key Insights

| Insight | Observation |
|----------|--------------|
| **Men vs Women** | Men tend to say “yes” more often, but overestimate matches. |
| **Common ground** | Shared interests have minimal influence. |
| **Demographics** | Age, income, religion, race – no measurable effect. |
| **Personality traits** | Intelligence and sincerity slightly increase “yes” decisions. |
| **Optimism** | Expected happiness is the **best predictor** of positive outcomes. |

---

## 🧠 Conclusion
> This study identifies the factors most correlated with yes-decisions,  
> but no single clear determinant emerged — except for **optimism** and **expected happiness** in meeting someone.

Human connection remains complex and cannot be fully explained by demographic or surface-level traits — people’s **mindset and expectations** play the greatest role.

---

## 🧰 Tools & Libraries
- **Python**
- **Pandas**, **NumPy**
- **Matplotlib**, **Seaborn**
- **Jupyter Notebook**
- **VS Code**



