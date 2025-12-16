import pandas as pd
import statsmodels.formula.api as smf

df_long= pd.read_csv("test.csv")
print(df_long.columns.tolist())

#exit()
#Model_1= smf.mixedlm("WER ~ Group", df, groups=df["STEM"]) #having only STEM group as a random effect
model = smf.mixedlm(
    formula="wer ~ group",
    data=df_long,
    groups=df_long["participant"],  # Random effect for each participant
    vc_formula={"stem": "0 + C(stem)"}  # Random effect for each STEM topic
)
result = model.fit()
print(result.summary())

# Print random effects variance components
print("\n" + "="*60)
print("RANDOM EFFECTS VARIANCE COMPONENTS:")
print("="*60)
print(f"Participant variance: {result.cov_re.iloc[0, 0]:.4f}")
if "stem" in result.cov_vc:
    print(f"STEM variance: {result.cov_vc['stem']:.4f}")
print("="*60)


