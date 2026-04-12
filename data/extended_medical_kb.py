# Extended medical knowledge base — 25+ condition profiles
# Sources: NHS, NIH, PubMed, NICE guidelines

DOCS = [
    {
        "category": "Mental Health",
        "condition": "Depression",
        "source_url": "https://www.nhs.uk/mental-health/conditions/depression/overview/",
        "text": """Depression is a medical condition causing persistent low mood, loss of enjoyment, and fatigue lasting weeks or more. It's not a mood or a weakness — brain chemistry is involved and it responds well to treatment.

Symptoms include: persistent sadness or emptiness, loss of interest in activities, fatigue, poor concentration, changes in appetite and sleep, feelings of worthlessness, and in severe cases thoughts of self-harm or suicide.

Treatment options with strong evidence: CBT (cognitive behavioural therapy), antidepressants such as SSRIs, or a combination of both. Regular exercise has evidence comparable to medication in mild-to-moderate cases. Structured sleep routines and reducing alcohol also help.

If someone has thoughts of suicide or self-harm, contact a crisis line (UK: Samaritans 116 123, free 24/7) or go to A&E. Recovery is possible — most people respond well to treatment, especially when started early."""
    },
    {
        "category": "Mental Health",
        "condition": "Generalised Anxiety Disorder",
        "source_url": "https://www.nhs.uk/mental-health/conditions/generalised-anxiety-disorder/overview/",
        "text": """GAD involves persistent, hard-to-control worry about many situations — not just one specific thing. It affects roughly 1 in 20 people and often co-occurs with depression.

Symptoms: excessive worry that feels impossible to stop, muscle tension, restlessness, fatigue, difficulty concentrating, irritability, poor sleep, headaches, and nausea.

Self-management that helps: diaphragmatic breathing, structured worry time (15 minutes daily to write down worries), regular aerobic exercise, limiting caffeine, and consistent sleep.

Evidence-based treatment: CBT is the most effective psychological treatment. SSRIs such as sertraline are effective medical options. Mindfulness-based approaches also have growing evidence.

See a GP if anxiety is significantly affecting work, relationships, or daily life."""
    },
    {
        "category": "Mental Health",
        "condition": "Insomnia",
        "source_url": "https://www.nhs.uk/conditions/insomnia/",
        "text": """Insomnia is difficulty falling or staying asleep that affects daytime functioning. It's chronic when it occurs 3+ nights a week for 3+ months.

Common causes: stress, irregular sleep schedule, caffeine, alcohol, shift work, pain, mental health conditions, and certain medications.

CBT for Insomnia (CBT-I) is the most effective long-term treatment and is recommended before sleeping tablets. It includes sleep restriction, stimulus control (bed = sleep only), and cognitive techniques.

Sleep hygiene basics that genuinely help: consistent sleep/wake time every day including weekends, no caffeine after 2pm, cool dark quiet bedroom, no screens 30-60 minutes before bed, avoid alcohol within 3 hours of sleep.

Sleeping tablets may help short-term (2-4 weeks) but aren't appropriate long-term due to dependence risk."""
    },
    {
        "category": "Gastrointestinal",
        "condition": "GERD (Acid Reflux)",
        "source_url": "https://www.nhs.uk/conditions/acid-reflux/",
        "text": """GERD occurs when stomach acid repeatedly flows back into the oesophagus. Common symptoms: heartburn (burning in the chest, worse after eating and when lying down), regurgitation of sour liquid, difficulty swallowing, chronic cough, and hoarseness.

Lifestyle changes are the foundation: eat smaller meals, don't lie down for 2-3 hours after eating, raise the head of the bed, lose weight if overweight, reduce alcohol and caffeine, stop smoking.

Medications: antacids for occasional symptoms; H2 blockers (famotidine) for more regular symptoms; PPIs (omeprazole, lansoprazole) for persistent reflux — typically 4-8 weeks.

See a doctor if symptoms are severe, not responding to treatment, or accompanied by difficulty swallowing, weight loss, or signs of bleeding (dark stools, vomiting blood)."""
    },
    {
        "category": "Gastrointestinal",
        "condition": "Irritable Bowel Syndrome (IBS)",
        "source_url": "https://www.nhs.uk/conditions/irritable-bowel-syndrome-ibs/",
        "text": """IBS is a long-term gut condition causing recurring abdominal pain, bloating, and changes in bowel habits (diarrhoea, constipation, or both) without structural damage.

Contributing factors include gut hypersensitivity, altered gut-brain signalling, food intolerances (particularly FODMAPs), gut microbiome changes, previous gut infections, and stress.

The low-FODMAP diet has the strongest evidence for reducing symptoms — ideally guided by a dietitian. Other helpful approaches: regular exercise, stress management, probiotics (some Bifidobacterium species), and symptom-targeted medications (antispasmodics for cramping, loperamide for diarrhoea, laxatives for constipation).

CBT and gut-directed hypnotherapy have good evidence by addressing the gut-brain axis.

See a doctor if you have rectal bleeding, unexplained weight loss, persistent vomiting, or symptom onset after age 60 — these need investigation."""
    },
    {
        "category": "Cardiovascular",
        "condition": "Hypertension",
        "source_url": "https://www.nhs.uk/conditions/high-blood-pressure-hypertension/",
        "text": """High blood pressure (hypertension) is consistently above 140/90 mmHg in clinic or 135/85 at home. It usually causes no symptoms — which is why it's called the silent killer. Left untreated it significantly raises risk of stroke, heart attack, and kidney disease.

Lifestyle changes that make a real difference: reducing salt intake (most impactful dietary change), regular aerobic exercise, losing weight, limiting alcohol, and stopping smoking. The DASH diet has strong evidence.

If medication is prescribed, take it consistently even when feeling well — the whole point is preventing silent damage.

Get blood pressure checked at least every 5 years if over 40. If readings exceed 180/120 with symptoms (severe headache, chest pain, visual changes), seek same-day medical care."""
    },
    {
        "category": "Cardiovascular",
        "condition": "Atrial Fibrillation",
        "source_url": "https://www.nhs.uk/conditions/atrial-fibrillation/",
        "text": """AF is the most common heart rhythm disorder. The upper heart chambers beat irregularly, causing blood to pool and potentially clot — giving people with AF roughly five times the stroke risk of those without it.

Symptoms: palpitations (racing, fluttering, or irregular heartbeat), breathlessness, dizziness, fatigue. Some people have no symptoms at all.

Risk factors: older age, high blood pressure (most common modifiable risk), heart disease, diabetes, obesity, sleep apnoea, and excessive alcohol.

Management has two parts: rate/rhythm control (medications or procedures), and stroke prevention (anticoagulation with drugs like apixaban or rivaroxaban).

If you develop sudden one-sided weakness, facial drooping, or difficulty speaking — call emergency services immediately. These may be stroke symptoms."""
    },
    {
        "category": "Cardiovascular",
        "condition": "Stroke — Recognition and Prevention",
        "source_url": "https://www.nhs.uk/conditions/stroke/",
        "text": """A stroke happens when blood supply to part of the brain is cut off — either by a clot (ischaemic, 85% of cases) or bleeding (haemorrhagic).

FAST: Face drooping, Arm weakness, Speech difficulty — Time to call emergency services immediately. Also: sudden severe headache, vision loss, dizziness, or loss of balance.

Time is critical. Clot-dissolving medication (thrombolysis) works within 4.5 hours of symptom onset. Mechanical clot removal is available at specialist centres up to 24 hours.

A TIA (mini-stroke) resolves within hours but is a serious warning sign — urgent assessment can dramatically reduce subsequent stroke risk.

Prevention: control blood pressure (most important single factor), treat AF with anticoagulants, stop smoking, manage cholesterol and blood sugar, exercise regularly."""
    },
    {
        "category": "Musculoskeletal",
        "condition": "Osteoarthritis",
        "source_url": "https://www.nhs.uk/conditions/osteoarthritis/",
        "text": """Osteoarthritis is the most common form of arthritis — gradual wear of joint cartilage causing pain, stiffness, and reduced movement. Most commonly affects knees, hips, hands, and spine.

Symptoms: joint pain worse with activity and better with rest (in early stages), morning stiffness, reduced range of movement, swelling, and a grating sensation.

Exercise is the single most effective non-surgical treatment — both aerobic exercise and strengthening around the affected joint. Weight loss significantly reduces knee and hip pain.

Other approaches: topical NSAIDs applied to the joint (good evidence, fewer side effects than oral), physiotherapy, walking aids. Joint replacement is effective for severe OA that limits quality of life.

There's no treatment that reliably reverses cartilage loss, but symptoms can be well managed with the right combination of approaches."""
    },
    {
        "category": "Musculoskeletal",
        "condition": "Rheumatoid Arthritis",
        "source_url": "https://www.nhs.uk/conditions/rheumatoid-arthritis/",
        "text": """Rheumatoid arthritis is an autoimmune condition where the immune system attacks joint linings, causing inflammation and potential damage to cartilage and bone. Unlike osteoarthritis, it's symmetrical (same joints both sides) and systemic — it can affect the heart, lungs, and eyes.

Key features: symmetrical small joint involvement (especially hands and feet), morning stiffness lasting 30+ minutes, fatigue, and general malaise.

Early diagnosis and treatment matters — joint damage can begin within months. Blood tests (rheumatoid factor, anti-CCP) support diagnosis.

Treatment cornerstone: disease-modifying drugs (DMARDs), with methotrexate the most common first-line. Biologics (anti-TNF agents) are used when conventional DMARDs aren't enough. A treat-to-target approach aiming for remission has transformed outcomes."""
    },
    {
        "category": "Musculoskeletal",
        "condition": "Lower Back Pain",
        "source_url": "https://www.nhs.uk/conditions/back-pain/",
        "text": """Over 90% of lower back pain is non-specific — no single structural cause found. Most resolves within 4-6 weeks. The spine is robust and the pain usually comes from muscles or ligaments.

The most important thing: keep moving. Bed rest prolongs recovery. Gentle walking, light activity, and maintaining normal routine helps.

Red flags needing emergency assessment: loss of bladder or bowel control, saddle area numbness, progressive leg weakness alongside back pain. These are rare but need immediate investigation.

Self-help: heat packs, paracetamol or ibuprofen, gentle movement. Stress, anxiety, and low mood are among the strongest predictors of pain becoming chronic — these matter as much as physical factors.

Physiotherapy and structured exercise programmes are highly effective for chronic back pain."""
    },
    {
        "category": "Endocrine",
        "condition": "Hypothyroidism",
        "source_url": "https://www.nhs.uk/conditions/underactive-thyroid-hypothyroidism/",
        "text": """Hypothyroidism is when the thyroid gland doesn't produce enough thyroid hormone, slowing the body's metabolism. Most common cause in iodine-sufficient countries is Hashimoto's thyroiditis (autoimmune).

Symptoms develop gradually: fatigue, unexplained weight gain, feeling cold, constipation, dry skin and hair, low mood, brain fog, slow heart rate, and heavy periods in women.

Diagnosis: TSH blood test — elevated TSH confirms the thyroid is underactive.

Treatment is simple and effective: levothyroxine (synthetic T4) taken daily on an empty stomach. Dose adjusted based on TSH measured 6-8 weeks later. Most people live entirely normally once levels are stable.

Note: calcium, iron, soy, and some antacids interfere with levothyroxine absorption — take separately by several hours."""
    },
    {
        "category": "Endocrine",
        "condition": "PCOS",
        "source_url": "https://www.nhs.uk/conditions/polycystic-ovary-syndrome-pcos/",
        "text": """PCOS is a common hormonal condition affecting people with ovaries, typically during reproductive years. Diagnosed when 2 of 3 features are present: irregular periods, elevated androgens (or symptoms of it), or polycystic ovaries on ultrasound.

Common symptoms: irregular or absent periods, difficulty conceiving, excess hair growth on face/body, acne, oily skin, scalp hair thinning, and weight gain. Insulin resistance is present in up to 80% of cases.

Management depends on the main concern. For periods: combined oral contraceptive pill. For fertility: lifestyle changes and weight loss can restore ovulation; letrozole or clomifene stimulate it. For insulin resistance: balanced diet low in refined carbs, regular exercise, and sometimes metformin.

Even 5-10% weight loss in those with overweight can meaningfully improve symptoms. PCOS is a lifelong condition but very manageable."""
    },
    {
        "category": "Neurological",
        "condition": "Migraine",
        "source_url": "https://www.nhs.uk/conditions/migraine/",
        "text": """Migraine is a neurological condition — not just a bad headache. Attacks typically involve throbbing one-sided pain, nausea, and sensitivity to light and sound, lasting 4-72 hours. About 30% of people get aura beforehand (visual disturbances, tingling, or speech difficulties).

Common triggers: hormonal changes, stress, sleep disruption, certain foods (alcohol, aged cheese), dehydration, and bright lights.

Acute treatment: take it early. Triptans (sumatriptan) work best for migraines specifically. NSAIDs and paracetamol help for milder attacks. Antiemetics help with nausea.

Preventive treatment (for 4+ attacks per month): beta-blockers, amitriptyline, topiramate, or newer CGRP inhibitors (erenumab, fremanezumab). Keeping a headache diary helps identify patterns.

Seek emergency help for: sudden severe "thunderclap" headache, headache with fever/stiff neck/rash/confusion/weakness, or first headache after age 50."""
    },
    {
        "category": "Neurological",
        "condition": "Epilepsy",
        "source_url": "https://www.nhs.uk/conditions/epilepsy/",
        "text": """Epilepsy is a tendency to have recurrent unprovoked seizures caused by abnormal electrical activity in the brain. Seizures vary widely — from brief staring spells (absence seizures) to full convulsions (tonic-clonic). Epilepsy is diagnosed after 2+ unprovoked seizures.

About 70% of people achieve seizure control with anti-seizure medication. First-line options include sodium valproate, lamotrigine, levetiracetam, and carbamazepine — choice depends on seizure type, age, and individual factors.

Seizure first aid: don't restrain the person, don't put anything in their mouth, protect their head, roll onto their side when convulsions stop, stay with them. Call 999 if: the seizure lasts more than 5 minutes, they don't regain consciousness, or a second seizure follows immediately.

Important safety considerations: driving restrictions apply (discuss with doctor and DVLA), avoid unsupervised swimming, and identify personal triggers (sleep deprivation is common)."""
    },
    {
        "category": "Dermatological",
        "condition": "Eczema (Atopic Dermatitis)",
        "source_url": "https://www.nhs.uk/conditions/atopic-eczema/",
        "text": """Atopic eczema is a chronic inflammatory skin condition causing dry, itchy, inflamed skin. It's part of the atopic triad (with asthma and hay fever), runs in families, and is not contagious.

Symptoms: intense itch (worse at night), dry cracked skin, red or grey-brown patches, weeping bumps when scratched. In adults it commonly affects the creases of elbows, knees, neck, and hands.

Common triggers: soaps, detergents, synthetic fabrics, sweat, pet dander, dust mites, stress, and certain foods (especially in young children).

The most important management is emollient therapy: apply thick unperfumed moisturiser generously 2+ times daily and immediately after bathing. Use as a soap substitute.

For flares: topical corticosteroids on inflamed areas. For severe or frequent flares: a GP or dermatologist can prescribe stronger treatments or biologics like dupilumab.

Seek same-day advice if eczema looks infected (weeping, crusting, increased redness, warmth, fever)."""
    },
    {
        "category": "Dermatological",
        "condition": "Psoriasis",
        "source_url": "https://www.nhs.uk/conditions/psoriasis/",
        "text": """Psoriasis is a chronic autoimmune skin condition causing accelerated skin cell turnover, leading to raised red or salmon-coloured plaques with silvery scales. Most commonly affects elbows, knees, scalp, and lower back.

It's not contagious. Genetic predisposition plays a significant role.

Common triggers: stress, certain medications (beta-blockers, lithium, some NSAIDs), streptococcal infections, skin injury, smoking, and alcohol.

Up to 30% of people with psoriasis develop psoriatic arthritis — joint pain and stiffness that needs separate assessment and treatment.

Treatment is stepped: mild — topical corticosteroids, vitamin D analogues (calcipotriol), coal tar; moderate-to-severe — phototherapy, systemic agents (methotrexate, ciclosporin), or biologics (TNF inhibitors, IL-17/IL-23 inhibitors) which are highly effective. Emollients reduce scaling and itch throughout all stages."""
    },
    {
        "category": "Respiratory",
        "condition": "COPD",
        "source_url": "https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/",
        "text": """COPD is a group of progressive lung diseases (primarily emphysema and chronic bronchitis) that obstruct airflow. 80-90% of cases are caused by smoking. Symptoms typically develop gradually: increasing breathlessness, persistent cough with mucus, frequent chest infections, and wheezing.

Spirometry confirms the diagnosis — a post-bronchodilator FEV1/FVC below 0.70.

Stopping smoking is the only thing that reliably slows lung function decline. Everything else manages symptoms. Medications: short-acting bronchodilators for relief, long-acting bronchodilators for maintenance, inhaled corticosteroids for those with frequent exacerbations.

Pulmonary rehabilitation — structured exercise and education — is one of the most effective interventions for improving quality of life and reducing hospital admissions.

Annual influenza and pneumococcal vaccination are strongly recommended. Exacerbations triggered by infections can be life-threatening in advanced COPD."""
    },
    {
        "category": "Infectious",
        "condition": "Urinary Tract Infections (UTI)",
        "source_url": "https://www.nhs.uk/conditions/urinary-tract-infections-utis/",
        "text": """UTIs are bacterial infections in the urinary system — urethra, bladder (cystitis), or kidneys (pyelonephritis). E. coli causes ~80% of cases. They're much more common in women — about 50% will have at least one in their lifetime.

Lower UTI symptoms: burning when urinating, frequent urgency with little urine, cloudy or strong-smelling urine, lower abdominal pain, and sometimes blood in the urine.

Upper UTI (kidney infection) symptoms are more serious: high fever, back or flank pain, nausea and vomiting. This needs prompt antibiotic treatment.

Treatment: uncomplicated lower UTIs need 3-7 days of antibiotics (nitrofurantoin or trimethoprim are common first-line choices). Drink plenty of fluids.

Prevention: stay hydrated, urinate after sex, avoid harsh soaps around the genital area.

Recurrent UTIs (3+ per year) warrant further investigation."""
    },
    {
        "category": "Infectious",
        "condition": "Influenza",
        "source_url": "https://www.nhs.uk/conditions/flu/",
        "text": """Flu comes on suddenly and hits harder than a cold — high fever, severe muscle aches, exhaustion, dry cough, headache, and sore throat. Most healthy adults recover in about a week, though fatigue can linger for 2-3 weeks.

Complications (including bacterial pneumonia) are more likely in older adults, young children, pregnant women, and those with chronic conditions.

Treatment: rest and fluids are the foundations. Paracetamol or ibuprofen for fever and pain. Antivirals (oseltamivir) reduce illness by 1-2 days if started within 48 hours — mainly recommended for high-risk groups.

Prevention: annual flu vaccination is strongly recommended for anyone at higher risk. Hand hygiene and covering coughs help reduce spread.

Seek urgent care if breathing becomes severely difficult, chest pain develops, or symptoms markedly worsen after initial improvement."""
    },
    {
        "category": "Hematological",
        "condition": "Iron Deficiency Anaemia",
        "source_url": "https://www.nhs.uk/conditions/iron-deficiency-anaemia/",
        "text": """Iron deficiency anaemia is the most common anaemia worldwide — not enough iron to make adequate haemoglobin means less oxygen reaches the body's tissues.

Symptoms: fatigue, shortness of breath on exertion, palpitations, pale skin and inner eyelids, headaches, dizziness, cold extremities, brittle nails, and hair loss. Many people have mild anaemia without realising.

Common causes: heavy periods (most common in women of reproductive age), inadequate dietary intake, pregnancy, or GI blood loss (in men and post-menopausal women — this needs investigation to find the cause).

Diagnosis: low haemoglobin + low serum ferritin (most sensitive marker of iron stores).

Treatment: oral iron supplements (ferrous sulfate). Taken on empty stomach improves absorption but worsens GI side effects. Vitamin C alongside iron enhances absorption. Iron-rich foods: red meat, shellfish, beans, fortified cereals, leafy greens (plant iron is less well absorbed — pair with vitamin C)."""
    },
    {
        "category": "Renal",
        "condition": "Kidney Stones",
        "source_url": "https://www.nhs.uk/conditions/kidney-stones/",
        "text": """Kidney stones are hard deposits forming inside the kidneys. When a stone moves into the ureter it causes ureteric colic — one of the most severe pains possible. Symptoms: sudden severe flank pain radiating to the groin, nausea, vomiting, blood in urine, and painful urination.

Most stones (80%) are calcium oxalate. Risk factors: dehydration (the main modifiable one), high-salt or high-protein diet, oxalate-rich foods, gout, and obesity.

Stones under 5mm often pass on their own with adequate hydration and pain relief. NSAIDs work well for the pain. Larger or obstructing stones need ureteroscopy, lithotripsy, or surgery.

Recurrence prevention: drink enough to produce 2 litres of urine daily — this is the single most important measure. Reducing salt and animal protein intake also helps."""
    },
    {
        "category": "Other",
        "condition": "Vitamin D Deficiency",
        "source_url": "https://www.nhs.uk/conditions/vitamins-and-minerals/vitamin-d/",
        "text": """Vitamin D is made primarily through skin exposure to UVB sunlight. It's essential for calcium absorption, bone health, immune function, and muscle function. Deficiency is very common, particularly in autumn/winter in northern countries.

At-risk groups: people who cover most skin, older adults, those with darker skin, housebound people, those with obesity or malabsorption conditions.

Symptoms of deficiency: often none specific — fatigue, bone pain, muscle weakness, low mood, and frequent infections. Severe prolonged deficiency causes rickets in children and osteomalacia (soft bones) in adults.

Diagnosis: serum 25(OH)D blood test.

Supplementation: vitamin D3 (colecalciferol) is preferred. UK guidance: 10 micrograms (400 IU) daily for general prevention in autumn/winter; higher doses for confirmed deficiency. Dietary sources (oily fish, eggs, fortified foods) are rarely sufficient alone."""
    },
    {
        "category": "Other",
        "condition": "Obesity and Weight Management",
        "source_url": "https://www.nhs.uk/conditions/obesity/",
        "text": """Obesity (BMI 30+) results from a complex mix of genetics, environment, psychology, and biology — not simply willpower. Waist circumference matters too: above 88cm in women and 102cm in men significantly raises health risk.

Health risks: type 2 diabetes, cardiovascular disease, several cancers, sleep apnoea, fatty liver disease, osteoarthritis, and depression.

What works: a sustained calorie deficit through improved diet quality (focus on whole foods, fewer ultra-processed products) combined with physical activity. The Mediterranean diet pattern has the best cardiovascular evidence. Behaviour change programmes with self-monitoring consistently improve outcomes.

Even 5-10% weight loss produces meaningful health benefits. Rapid weight loss typically doesn't stick — sustainable habits matter more.

Medications (GLP-1 agonists like semaglutide) and bariatric surgery are options for those with higher BMI or significant comorbidities where lifestyle changes haven't been sufficient."""
    },
    {
        "category": "Other",
        "condition": "Allergies",
        "source_url": "https://www.nhs.uk/conditions/allergies/",
        "text": """An allergy is an abnormal immune response to a harmless substance (allergen). Common allergens: pollen, dust mites, animal dander, certain foods (nuts, milk, eggs, fish), insect stings, latex, and medications.

Reactions range from mild (sneezing, runny nose, hives, eczema) to severe anaphylaxis — a life-threatening reaction causing throat swelling, breathing difficulty, and a sudden drop in blood pressure.

Anaphylaxis: call emergency services immediately. If the person has an adrenaline auto-injector (EpiPen), use it. Do not wait to see if symptoms improve.

Management: identify and avoid triggers. For allergic rhinitis: intranasal corticosteroid sprays work best, antihistamines for acute symptoms. For food allergies: strict avoidance, carry an adrenaline auto-injector if at risk, have an emergency action plan.

Allergen immunotherapy (desensitisation) is available for pollen, dust mite, bee/wasp venom, and increasingly for peanut allergy."""
    },
]


def get_all_documents():
    return [
        {
            "question": f"What is {d['condition']}?",
            "answer": d["text"],
            "source_url": d["source_url"],
            "category": d["category"],
        }
        for d in DOCS
    ]


if __name__ == "__main__":
    docs = get_all_documents()
    print(f"{len(docs)} documents in extended knowledge base:")
    for d in docs:
        print(f"  [{d['category']}] {d['question']}")
