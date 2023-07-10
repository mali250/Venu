from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from flask_cors import CORS
from googletrans import Translator
from deep_translator import GoogleTranslator

app = Flask(__name__)
CORS(app)

english_bot = ChatBot("Chatterbot", storage_adapter="chatterbot.storage.SQLStorageAdapter",
                     logic_adapters=[
                         'chatterbot.logic.MathematicalEvaluation',
                         'chatterbot.logic.BestMatch'
                     ])

# training the chatbot
small_convo = [
    'Hi there!',
    'Hi',
    'How do you do?',
    'How are you?',
    'I\'m cool.',
    'Always cool.',
    'I\'m Okay',
    'Glad to hear that.',
    'I\'m fine',
    'I feel awesome',
    'Excellent, glad to hear that.',
    'Not so good',
    'Sorry to hear that.',
    'What\'s your name?',
    ' I\'m AI BOT. Ask me any question, please.'
]

convo_1 = [
    'What is the OASI',
    'The OASI is the state pension plan. It guarantees coverage of basic needs to the entire population. The law prescribes the amount of contributions, the benefits to be paid and how they are calculated. If income in the form of pensions is not enough to ensure livelihood, supplementary benefits are paid in order to cover vital needs.'
]

convo_2 = [
    'How does the OASI work',
    'State old-age provision is regulated under the pay-as-you-go system: money paid into the OASI is transferred from active members directly to retirees, without being set aside. The pay-as-you-go system has a great advantage: since the income is immediately passed on to the beneficiaries, interest trends and inflation are of marginal importance. However, the system also has some disadvantages: if the number of annuitants increases relative to the number of contributors, there is a risk of an imbalance between income and expenditure. The distribution system is also highly dependent on economic trends: if this is positive and the sum of wages increases, the OASI contribution base increases; on the contrary, in periods of crisis with high unemployment and low wages, income decreases and there is therefore a risk that the insurance will register deficits.'
]

convo_3 = [
    'When was the last OASI reform',
    'The last reform (21) was accepted by the People on September 25, 2022, thus guaranteeing the financing of OASI until 2030. OASI reform 21 will take effect on January 1, 2024. Both the amendment to the LAVS and the federal decree on supplementary financing of the OASI by increasing the value-added tax were approved.The two projects were related. The financing of the OASI and the level of pensions are thus guaranteed for the next ten years. The reference age will thus be set at 65 for both men and women, pension collection will be made more flexible, and the value-added tax (VAT) will be slightly increased. On December 9, 2022, the Federal Council set an effective date of January 1, 2024. It also placed the implementing provisions for consultation. The procedure will last until March 24, 2023']

convo_4 = [
    'How much is the coordination deduction',
    'In the second pillar, the coordination deduction amounts to 25725 francs.']

convo_5 = [
    'How much are the contributions in the second pillar',
    'The law requires that each insured person be credited with a certain percentage of the coordinated salary each year. These are the retirement credits, the amount of which depends on the age of the insured. 25-34 years old: 7%.35-44 years old: 10%.45-54 years old: 15%.55-65 years old: 18%.']

convo_6 = [
    'How is the OASI pension calculated',
    '''The amount of the OASI pension depends on two factors: how long OASI contributions were paid and how much the average annual income was.''']
convo_7 = [
    'How much can I pay into Pillar 3A',
    '''Those affiliated with a pension fund (generally employees): may make maximum contributions for the year 2023 of CHF 7056/year. For those not affiliated with a pension fund (generally self-employed): may make contributions equal to 20% of income, but up to a maximum of CHF 35,280/year.''']

convo_8 = [
    'What are the eligibility requirements for receiving OASI benefits?',
    '''To be eligible for OASI benefits, an individual must have paid into the system for a certain number of years, typically 10 years for Swiss citizens and 20 years for foreign nationals. Additionally, the individual must have reached the statutory retirement age, which is currently 65 for both men and women.''']

convo_9 = [
    'Can individuals choose to opt out of OASI contributions?',
    '''No, individuals cannot opt out of OASI contributions. It is mandatory for all employees and employers in Switzerland to contribute to the OASI system, unless they are exempted under certain circumstances such as being self-employed.''']

convo_10 = [
    'How are OASI benefits calculated?',
    '''The amount of OASI benefits an individual receives is based on their average annual income and the number of years they have contributed to the system. The formula for calculating OASI benefits is complex, but in general, the more years an individual contributes and the higher their average income, the higher their benefit amount will be.''']
convo_11 = [
    'What are the different types of supplementary benefits available through OASI?',
    '''In addition to the basic OASI pension, there are several types of supplementary benefits available to individuals who do not have enough income to cover their vital needs. These include disability benefits, survivor benefits, and supplementary benefits for individuals who are not eligible for the basic OASI pension.''']
convo_12 = [
    'How is the OASI system funded?',
    '''The OASI system is primarily funded through payroll contributions from employees and employers, as well as self-employed individuals. In addition, the Swiss government provides some funding to the OASI system, and there are also some taxes and fees that contribute to the system's revenue.''']
convo_13 = [
    'How has the demographic shift in Switzerland impacted the OASI system?',
    '''As the population of Switzerland ages and the birth rate declines, there are fewer active workers contributing to the OASI system relative to the number of retirees receiving benefits. This can create a financial strain on the system, as there may not be enough revenue to pay out all the benefits owed to retirees.''']
convo_14 = [
    'Are there any exceptions to the retirement age requirement for receiving OASI benefits?',
    '''Yes, there are some exceptions to the retirement age requirement. For example, individuals who are unable to work due to a disability may be eligible for OASI disability benefits before they reach the retirement age. Additionally, individuals who have contributed to the OASI system for at least 43 years may be eligible to retire early and receive full OASI benefits.''']
convo_15 = [
    'How do contributions to the second pillar (occupational pension) system work?',
    '''Switzerland, contributions to the second pillar pension system are typically split between the employee and the employer. The amount of the contribution is a percentage of the employee's salary, up to a certain limit. The exact percentage and limit vary depending on the individual's age and the terms of their employment contract.''']
convo_16 = [
    'Can individuals choose their own pension provider for the second pillar system?',
    '''Yes, individuals are free to choose their own pension provider for the second pillar system. They can either select a provider recommended by their employer or choose their own provider independently.''']
convo_17 = [
    "What happens to an individual's second pillar pension if they leave their job?",
    '''If an individual leaves their job, they have several options for their second pillar pension. They can either transfer the funds to a new pension plan with their new employer, leave the funds with their previous pension plan, or withdraw the funds as a lump sum (although this option may have tax implications).''']
convo_18 = [
    'How has the demographic shift in Switzerland impacted the OASI system?',
    '''As the population of Switzerland ages and the birth rate declines, there are fewer active workers contributing to the OASI system relative to the number of retirees receiving benefits. This can create a financial strain on the system, as there may not be enough revenue to pay out all the benefits owed to retirees.''']
convo_19 = [
    'Are there any exceptions to the retirement age requirement for receiving OASI benefits?',
    '''Yes, there are some exceptions to the retirement age requirement. For example, individuals who are unable to work due to a disability may be eligible for OASI disability benefits before they reach the retirement age. Additionally, individuals who have contributed to the OASI system for at least 43 years may be eligible to retire early and receive full OASI benefits.''']
convo_20 = [
    'How do contributions to the second pillar (occupational pension) system work?',
    '''In Switzerland, contributions to the second pillar pension system are typically split between the employee and the employer. The amount of the contribution is a percentage of the employee's salary, up to a certain limit. The exact percentage and limit vary depending on the individual's age and the terms of their employment contract.''']
convo_21 = [
    'Can individuals choose their own pension provider for the second pillar system',
    '''Yes, individuals are free to choose their own pension provider for the second pillar system. They can either select a provider recommended by their employer or choose their own provider independently.''']
convo_22 = [
    "What happens to an individual's second pillar pension if they leave their job.",
    '''If an individual leaves their job, they have several options for their second pillar pension. They can either transfer the funds to a new pension plan with their new employer, leave the funds with their previous pension plan, or withdraw the funds as a lump sum (although this option may have tax implications).''']
convo_23 = [
    'How is the amount of OASI benefits calculated?',
    '''The amount of OASI benefits is calculated based on the individual's average income over their working life, as well as the number of years they have contributed to the system.''']
convo_24 = [
    'How long must an individual have lived in Switzerland to be eligible for OASI benefits?',
    '''An individual must have lived in Switzerland for at least 10 years to be eligible for OASI benefits.''']

convo_25 = [
    'What is the current retirement age in Switzerland',
    '''The current retirement age in Switzerland is 65 for both men and women.''']

convo_26 = [
    'What is the minimum and maximum amount of OASI benefits an individual can receive?',
    '''The minimum amount of OASI benefits an individual can receive is 1170 CHF per month, and the maximum amount is currently 2350 CHF per month.''']
convo_27 = [
    'Can individuals receive both OASI and disability benefits at the same time',
    '''No, individuals cannot receive both OASI and disability benefits at the same time.''']

convo_28 = [
    'How is the coordination deduction calculated in the second pillar system?',
    '''The coordination deduction in the second pillar system is calculated based on the amount of the individual's primary insurance benefit under the first pillar system (OASI).''']
convo_29 = [
    'How do individuals apply for OASI benefits',
    '''Individuals can apply for OASI benefits by contacting their local OASI office and submitting an application form.''']
convo_30 = [
    'Can individuals receive OASI benefits while living abroad',
    '''Yes, individuals can receive OASI benefits while living abroad, as long as they meet certain eligibility criteria.''']
convo_31 = [
    'What is the purpose of the AHV/AVS number?',
    '''The AHV/AVS number is a unique identifier assigned to each individual who is registered with the OASI system. It is used to track contributions and benefits.''']
convo_32 = [
    'Can individuals receive OASI benefits if they have never worked in Switzerland',
    '''In some cases, yes. Individuals who are Swiss citizens or who have lived in Switzerland for at least 20 years may be eligible for OASI benefits even if they have never worked in Switzerland.''']
convo_33 = [
    'What is the difference between OASI and disability benefits',
    '''OASI benefits are provided to individuals who have reached retirement age and are no longer working, while disability benefits are provided to individuals who are unable to work due to a disability.''']
convo_34 = [
    'What is the second pillar system in Switzerland',
    '''The second pillar system in Switzerland is a mandatory occupational pension system, which is designed to supplement the OASI system.''']
convo_35 = [
    'How are second pillar pension benefits calculated',
    '''The amount of second pillar pension benefits is based on the individual's salary, the length of their employment, and the amount of contributions made to the pension plan.''']
convo_36 = [
    'How are second pillar pension benefits calculated',
    '''The amount of second pillar pension benefits is based on the individual's salary, the length of their employment, and the amount of contributions made to the pension plan.''']
convo_37 = [
    'Can individuals choose how their second pillar contributions are invested?',
    '''Yes, individuals can choose how their second pillar contributions are invested by selecting from a range of investment options offered by their pension provider''']
convo_38 = [
    'What is the third pillar system in Switzerland',
    '''The third pillar system in Switzerland is a voluntary individual pension savings system, which is designed to supplement the OASI and second pillar systems.''']
convo_39 = [
    'How do contributions to the third pillar system work',
    '''Contributions to the third pillar system are made on a voluntary basis, and individuals can choose how much they want to contribute each year, up to certain limits.''']
convo_40 = [
    'Can individuals withdraw money from their third pillar savings before retirement?',
    '''Yes, individuals can withdraw money from their third pillar savings before retirement, but there may be tax implications for doing so.''']
convo_41 = [
    'What is the difference between the second and third pillar systems',
    '''The second pillar system is a mandatory occupational pension system, while the third pillar system is a voluntary individual pension savings system.''']
convo_42 = [
    'Can individuals contribute to both the second and third pillar systems',
    '''Yes, individuals can contribute to both''']
convo_43 = [
    'What is the AHV?',
    '''AHV stands for "Alters- und Hinterlassenenversicherung" in German, which means "Old Age and Survivors Insurance" in English. It is a social security system in Switzerland that provides basic financial support to retired people, disabled people, and surviving dependents of deceased insured individuals.''']
convo_44 = [
    'What is the IV',
    '''The IV stands for "Invalidenversicherung" in German, which means "Disability Insurance" in English. It is a social security system in Switzerland that provides financial support to people with disabilities.''']

convo_45 = [
    'How is the AHV funded',
    '''The AHV is funded through contributions from employers, employees, and self-employed individuals. The contribution rate is currently 8.7% of an individual's salary, up to a certain maximum amount.''']
convo_46 = [
    'What is the maximum AHV contribution',
    '''The maximum AHV contribution for an individual is currently CHF 24,885 per year.''']
convo_47 = [
    'How is the IV funded',
    '''The IV is funded through contributions from employers, employees, and self-employed individuals. The contribution rate is currently 1.4% of an individual's salary, up to a certain maximum amount.''']
convo_48 = [
    'What is the maximum IV contribution',
    '''The maximum IV contribution for an individual is currently CHF 4,860 per year.''']

convo_49 = [
    'What is the purpose of the BVG',
    '''The BVG is the "Berufliche Vorsorge" in German, which means "Occupational Pension" in English. Its purpose is to provide retirement, disability, and survivor benefits to employees in Switzerland.''']

convo_50 = [
    'Who is covered by the BVG',
    '''All employees in Switzerland who earn more than CHF 21,510 per year and are under the age of 25 are covered by the BVG.''']

convo_51 = [
    'What is the minimum BVG contribution',
    '''The minimum BVG contribution is 7% of an employee's salary, up to a certain maximum amount.''']

convo_52 = [
    "What is the maximum BVG contribution",
    '''The maximum BVG contribution is currently CHF 85,320 per year.''']

convo_53 = [
    'What is the minimum IV contribution',
    '''The minimum IV contribution for an individual is currently CHF 482 per year.''']

convo_54 = [
    'How is the BVG contribution split between employers and employees',
    '''The BVG contribution is split evenly between employers and employees, with each party contributing 50% of the total amount.''']

convo_55 = [
    'What is the difference between the first and second pillar of the Swiss pension system?',
    '''The first pillar of the Swiss pension system consists of the AHV/IV, which provides a basic income to retirees, disabled individuals, and surviving dependents of deceased insured individuals. The second pillar consists of occupational pension schemes, which provide additional retirement, disability, and survivor benefits to employees''']

convo_56 = [
    'What is the third pillar of the Swiss pension system',
    '''The third pillar of the Swiss pension system consists of private retirement savings plans, which individuals can use to supplement their income in retirement.''']

convo_57 = [
    'What is the purpose of the third pillar of the Swiss pension system',
    '''The purpose of the third pillar is to allow individuals to save additional funds for retirement beyond what is provided by the first and second pillars.''']

convo_58 = [
    'What is the tax benefit of contributing to a third pillar pension plan',
    '''Contributions to third pillar pension plans are tax-deductible, which means that individuals can reduce their taxable income by the amount of their contribution.''']

convo_59 = [
    'What is the maximum retirement age for OASI benefits',
    '''The maximum retirement age for OASI benefits is currently set at 70 years old''']

convo_60 = [
    'How is the amount of OASI benefits calculated?',
    '''The amount of OASI benefits is calculated based on an individual's average earnings over their career and the number of years they have contributed to the system. The formula for calculating OASI benefits is complex and takes into account a variety of factors.''']
convo_61 = [
    'What is the minimum retirement age for OASI benefits?',
    '''The minimum retirement age for OASI benefits is currently set at 65 years old for both men and women''']
convo_62 = [
    'How are OASI contributions calculated?',
    '''OASI contributions are calculated as a percentage of an individual's income, with both employers and employees required to contribute. The exact percentage varies depending on the individual's income level.''']
convo_63 = [
    'What is the purpose of the coordination deduction in the second pillar?',
    '''The purpose of the coordination deduction in the second pillar is to ensure that individuals do not receive excessive retirement benefits by having multiple sources of income in retirement.''']
convo_64 = [
    'What is the purpose of the second pillar in the Swiss pension system?',
    '''The purpose of the second pillar in the Swiss pension system is to provide additional retirement benefits beyond those provided by the OASI''']
convo_65 = [
    'How are contributions to the second pillar tax-deductible?',
    '''Contributions to the second pillar are tax-deductible up to a certain limit, which varies depending on the individual's income level.''']
convo_66 = [
    'How are the retirement credits in the second pillar calculated?',
    '''The retirement credits in the second pillar are calculated as a percentage of an individual's salary, with the percentage increasing as the individual gets older.''']
convo_67 = [
    'What is the purpose of the third pillar in the Swiss pension system?',
    '''The purpose of the third pillar in the Swiss pension system is to provide additional retirement benefits beyond those provided by the OASI and the second pillar.''']
convo_68 = [
    'What is the difference between the third pillar and the second pillar in the Swiss pension system',
    '''The third pillar is a voluntary retirement savings plan, while the second pillar is a mandatory employer-provided retirement savings plan.''']
convo_69 = [
    'How are contributions to the third pillar taxed',
    '''Contributions to the third pillar are tax-deductible up to a certain limit, which varies depending on the individual's income level.''']
convo_71 = [
    'What is the purpose of the BVG minimum interest rate',
    '''The purpose of the BVG minimum interest rate is to ensure that retirement benefits in the second pillar keep pace with inflation''']
convo_72 = [
    'What is the current BVG minimum interest rate?',
    '''The current BVG minimum interest rate is 1%.''']
convo_73 = [
    'What is the purpose of the BVG maximum conversion rate',
    '''The purpose of the BVG maximum conversion rate is to ensure that retirement benefits in the second pillar are not excessively high.''']
convo_74 = [
    'What is the current BVG maximum conversion rate',
    '''The current BVG maximum conversion rate is 6.8%.''']
convo_75 = [
    'What is the purpose of the BVG coordination deduction',
    '''The purpose of the BVG coordination deduction is to ensure that individuals do not receive excessive retirement benefits by having multiple sources of income in retirement.''']
convo_76 = [
    'What is the current BVG coordination deduction?',
    '''The current BVG coordination deduction is CHF 25,725.''']
convo_77 = [
    'How are contributions to the BVG calculated',
    '''Contributions to the BVG are calculated as a percentage of an individual's salary, with both employers and employees required to contribute.''']
convo_78 = [
    'How are retirement benefits in the second pillar paid out?',
    '''Retirement benefits in the second pillar are typically paid out in the form of a pension, which is based on the amount of''']

convo_79 = [
    'purpose of the BVG maximum conversion rate',
    '''The purpose of the BVG maximum conversion rate is to ensure that retirement benefits in the second pillar are not excessively high.''']

convo_80 = [
    'current BVG deduction',
    '''The current BVG coordination deduction is CHF 25,725.''']
convo_81 = [
    ' purpose of the BVG coordination deduction',
    '''The purpose of the BVG coordination deduction is to ensure that individuals do not receive excessive retirement benefits by having multiple sources of income in retirement.''']

convo_82 = [
    'difference between the third pillar and the second pillar in the Swiss pension system',
    '''The third pillar is a voluntary retirement savings plan, while the second pillar is a mandatory employer-provided retirement savings plan.''']
convo_83 = [
    ' OASI',
    'The OASI is the state pension plan. It guarantees coverage of basic needs to the entire population. The law prescribes the amount of contributions, the benefits to be paid and how they are calculated. If income in the form of pensions is not enough to ensure livelihood, supplementary benefits are paid in order to cover vital needs.'
]


#trainer = ChatterBotCorpusTrainer(english_bot)
#trainer.train("chatterbot.corpus.english")
# using the ListTrainer class
list_trainee = ListTrainer(english_bot)
for i in (small_convo, convo_1, convo_2, convo_3, convo_4, convo_5, convo_7, convo_8, convo_9, convo_10, convo_11, convo_12, convo_13, convo_14, convo_15
          , convo_16, convo_17, convo_18, convo_19, convo_20, convo_21, convo_22, convo_23, convo_24, convo_25, convo_26, convo_27, convo_28, convo_29, convo_30
          , convo_31, convo_32, convo_33, convo_34, convo_35, convo_36, convo_38, convo_39, convo_40, convo_41, convo_42, convo_43, convo_44, convo_45, convo_46,
          convo_47, convo_48, convo_49, convo_50, convo_51, convo_52, convo_53, convo_54, convo_55, convo_56, convo_57, convo_58, convo_59, convo_60, convo_61
          , convo_62, convo_63, convo_64, convo_65, convo_66, convo_67, convo_68, convo_69, convo_71, convo_72, convo_73, convo_74, convo_75, convo_76
          , convo_77, convo_78,convo_79,convo_80,convo_81,convo_82,convo_83):
    list_trainee.train(i)
    


from googletrans import Translator
translator = Translator()
from deep_translator import GoogleTranslator

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    message = data['message']
    #@print(message)
    to_translate = message
    translation = translator.translate(to_translate)
    print(translation)
    if translation.src == "en":
        return jsonify({'answer': english_bot.get_response(message).text})
    else:
        translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
        res = str(english_bot.get_response(translated))
        res2 = GoogleTranslator(source='en', target=translation.src).translate(res)
        return jsonify({'answer': res2})
  
     
     
if __name__ == '__main__':
    app.run()








