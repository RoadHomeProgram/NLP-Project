# NLP-Project

Example use:
```
(base) spohorence@seans-air preprocessing % python
Python 3.8.3 (default, Jul  2 2020, 11:26:31)
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from clinical_note import ClinicalNote, parse_clinical_note
>>> import pandas as pd
>>> df = pd.read_csv("../../data/DBMI/2014_heart_disease_risk_factors/summarized_heart_data.csv")
>>> note_text = df.iloc[0].text
>>> clinical_note = parse_clinical_note(note_text)
>>> clinical_note.annotate_note()
  1. Record date ->
    2093-01-13
  2. Team X Intern Admission Note
  3. Name ->
    Hendrickson, Ora
  4. MR# 		7194334
  5. Date ->
    01/13/93
  6. PCP ->
    Oliveira, Keith MD
  7. CC/RFA ->
    SOB.
  8. HPI ->
    Pt is a 76 yo F with a h/o CAD, HTN, hypercholesterolemia, COPD, CHF who developed acute SOB while at home PM of admission. Pt reports no dietary discretions and excellent adherence to medications. She was out evening of admission at a social gathering and noticed symptoms when she returned home and had difficulty climbing an internal staircase in her home She ascended the staircase and was unable to regain her breath. She reports she developed profound dyspnea and tachycardia. She denies chest pain, diaphoresis, dizziness or LOC. She has had a cough productive of clear sputum x 1 week with no fever, night sweats, rigors or chills during this time. She has had no vomiting or diarrhea. She does not recall wheezing, and asserts the only symptoms during the episode consisted in SOB and tachypnea.
```
