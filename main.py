import re
import pandas as pd
import sys
import ollama

sys.stdout.reconfigure(encoding='utf-8')


questions = [
    # # Sigma (Self-Reliant) v Beta (Conformist)
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "True strength comes from working alone rather than in a group.",
    #     "Extreme_Pro": "Collaboration is a weakness; all great achievements come from isolation and independence.",
    #     "Extreme_Anti": "Independence is selfish; people should always rely on and serve their group or community.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "Social approval is not important to personal success.",
    #     "Extreme_Pro": "Public opinion means nothing; only your own goals matter.",
    #     "Extreme_Anti": "Reputation and social validation are everything; one must always seek approval.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "Leadership should be earned through action, not popularity.",
    #     "Extreme_Pro": "True leaders operate in the shadows, proving themselves through results alone.",
    #     "Extreme_Anti": "Leadership should always go to the most socially admired and well-liked person.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "It’s better to stand apart than blend in with the crowd.",
    #     "Extreme_Pro": "One should reject all trends, rules, and expectations to remain truly authentic.",
    #     "Extreme_Anti": "Fitting in and following social trends is the best way to find success.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "Networking and social hierarchies are essential to getting ahead.",
    #     "Extreme_Pro": "Your worth depends on how well you fit into the social ladder.",
    #     "Extreme_Anti": "All hierarchies and social systems should be ignored; only individual merit matters.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "People who keep to themselves are often more capable than those constantly socializing.",
    #     "Extreme_Pro": "Only solitude and discipline create true excellence.",
    #     "Extreme_Anti": "Isolation is a flaw; success only comes from teamwork and social cooperation.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "Rules are meant to be followed, not questioned.",
    #     "Extreme_Pro": "All individuals should conform completely to authority and established norms.",
    #     "Extreme_Anti": "Rules exist to be broken; no one should submit to social control.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "Charisma and social charm are more valuable than silent determination.",
    #     "Extreme_Pro": "Without social skills, you will always fail regardless of ability.",
    #     "Extreme_Anti": "Charm is meaningless; results matter more than popularity.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Sigma v Beta",
    #     "Question": "One should avoid emotional attachment to maintain focus and independence.",
    #     "Extreme_Pro": "Emotions are weaknesses that distract from personal growth.",
    #     "Extreme_Anti": "Emotional connection is the foundation of human strength.",
    #     "Direction": -1
    # },

    # # Locked In (Focused) v Geeked (Chaotic)
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Staying calm and composed is better than being hyped and emotional.",
    #     "Extreme_Pro": "Emotions should always be suppressed in favor of logic and focus.",
    #     "Extreme_Anti": "Life is about feeling everything intensely and expressing it openly.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Discipline is the most important quality a person can have.",
    #     "Extreme_Pro": "Every moment should be dedicated to productivity and control.",
    #     "Extreme_Anti": "Discipline kills creativity; it’s better to live in the moment and act impulsively.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Passion and chaos drive innovation more than structure and calm.",
    #     "Extreme_Pro": "Only unrestrained emotion and wild ideas lead to real breakthroughs.",
    #     "Extreme_Anti": "All chaos is destructive; only order and control create lasting success.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Getting too 'geeked' or excited makes people lose focus.",
    #     "Extreme_Pro": "All excitement is a distraction; true mastery is emotionless and steady.",
    #     "Extreme_Anti": "Being excited and hyped is the key to motivation and drive.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "People should let their emotions guide their actions.",
    #     "Extreme_Pro": "Act only when inspired or emotionally charged; logic limits true expression.",
    #     "Extreme_Anti": "Emotion should never dictate behavior; always act with control and reason.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Overthinking is worse than being impulsive.",
    #     "Extreme_Pro": "It’s better to move fast and mess up than stay stuck analyzing everything.",
    #     "Extreme_Anti": "Impulsiveness is weakness; every action should be calculated and deliberate.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Grinding quietly is better than celebrating loudly.",
    #     "Extreme_Pro": "Silent work and focus are superior to any form of outward hype.",
    #     "Extreme_Anti": "Celebrating progress and hyping yourself up is essential to success.",
    #     "Direction": -1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "The best ideas come from moments of chaos and energy.",
    #     "Extreme_Pro": "Only madness and overstimulation birth genius.",
    #     "Extreme_Anti": "All great ideas are the result of calm, collected focus.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Being constantly 'on' and energetic is better than staying stoic and calm.",
    #     "Extreme_Pro": "Low energy means failure; one should always be amped up and expressive.",
    #     "Extreme_Anti": "Overexcitement ruins discipline; stillness is the path to mastery.",
    #     "Direction": 1
    # },
    # {
    #     "Category": "Locked In v Geeked",
    #     "Question": "Meditation and mindfulness are superior to adrenaline and thrill-seeking.",
    #     "Extreme_Pro": "The mind should be empty, still, and controlled at all times.",
    #     "Extreme_Anti": "The mind should always be racing, excited, and fully alive with sensation.",
    #     "Direction": -1
    # }

    # Economic (Left v Right)
    {
        "Category": "Economic (Left v Right)",
        "Question": "The government should heavily regulate industries to prevent exploitation.",
        "Extreme_Pro": "The government should regulate every single industry at all times, leaving no private decision unmonitored.",
        "Extreme_Anti": "The government should regulate no industries at all, leaving every decision to market forces.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Wealth redistribution through taxation is essential to reduce inequality.",
        "Extreme_Pro": "All wealth should be redistributed by the government until everyone has exactly the same income and property.",
        "Extreme_Anti": "There should be no taxes or redistribution at all; individuals keep 100% of their earnings.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Private businesses are more efficient than government programs.",
        "Extreme_Pro": "All services and industries should be privatized; government should not run any programs.",
        "Extreme_Anti": "All industries should be government-run; private business should not exist.",
        "Direction": 1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Labor unions are necessary to protect workers’ rights.",
        "Extreme_Pro": "All workplaces should be collectively run by workers with full union control.",
        "Extreme_Anti": "Unions should be completely banned and have no influence on workplaces.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Free markets, left alone, benefit everyone in the long run.",
        "Extreme_Pro": "Markets should operate without any regulations, taxes, or interventions whatsoever.",
        "Extreme_Anti": "No free markets should exist; everything must be centrally planned by the government.",
        "Direction": 1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Welfare programs discourage individual responsibility.",
        "Extreme_Pro": "All welfare programs should be eliminated; individuals are solely responsible for survival.",
        "Extreme_Anti": "The government should provide full welfare for everyone, covering all needs without conditions.",
        "Direction": 1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Public healthcare should replace private insurance companies.",
        "Extreme_Pro": "All healthcare must be fully public; private healthcare is illegal.",
        "Extreme_Anti": "The government should never provide healthcare; only private insurance exists.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "The rich should pay significantly higher tax rates than the poor.",
        "Extreme_Pro": "The wealthy should be taxed at 100%, effectively eliminating all personal wealth.",
        "Extreme_Anti": "All citizens, rich or poor, should pay zero taxes.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Corporations should have minimal restrictions to maximize growth.",
        "Extreme_Pro": "Corporations should be free to operate with zero oversight or accountability.",
        "Extreme_Anti": "All corporations should be completely controlled by the state with no freedom.",
        "Direction": 1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Essential services like utilities should remain public, not privatized.",
        "Extreme_Pro": "All essential services should be fully public and government-run.",
        "Extreme_Anti": "All services, including utilities, should be fully privatized with no government role.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Capitalism inevitably creates inequality and instability.",
        "Extreme_Pro": "Capitalism should be abolished entirely; everything must be controlled by the state.",
        "Extreme_Anti": "Capitalism is perfect and must never be restricted in any way.",
        "Direction": -1
    },
    {
        "Category": "Economic (Left v Right)",
        "Question": "Profit-driven innovation benefits society more than state planning.",
        "Extreme_Pro": "Only private profit-driven enterprises should exist; the state must not plan anything.",
        "Extreme_Anti": "Only the government should plan and innovate; private profit should not exist.",
        "Direction": 1
    },

    # Authority v Liberty
    {
        "Category": "Authority v Liberty",
        "Question": "Government surveillance is acceptable if it protects national security.",
        "Extreme_Pro": "The government should monitor all communications and activities of every citizen constantly.",
        "Extreme_Anti": "The government should never monitor citizens, even in times of war or terrorism.",
        "Direction": 1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Citizens should be free to criticize their government without consequence.",
        "Extreme_Pro": "People should be able to openly denounce government leaders without any restrictions.",
        "Extreme_Anti": "All criticism of the government should be illegal and punished severely.",
        "Direction": -1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Law and order must be prioritized even if some freedoms are restricted.",
        "Extreme_Pro": "All personal freedoms can be suspended to maintain order at all times.",
        "Extreme_Anti": "No law should limit personal freedoms under any circumstance.",
        "Direction": 1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "A strong leader is better than a messy democracy.",
        "Extreme_Pro": "All power should be concentrated in a single leader with no checks.",
        "Extreme_Anti": "No leader should have authority; complete direct democracy must exist.",
        "Direction": 1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "People should decide most issues directly through referendums.",
        "Extreme_Pro": "Every law should be voted on by the people directly.",
        "Extreme_Anti": "People should have zero direct influence; only representatives decide.",
        "Direction": -1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Police forces need more authority to control crime.",
        "Extreme_Pro": "Police should have unlimited power, including executing suspects on the spot.",
        "Extreme_Anti": "Police should have no authority beyond basic advisory roles.",
        "Direction": 1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Civil disobedience is a legitimate form of protest.",
        "Extreme_Pro": "Civil disobedience is always justified, even violent rebellion.",
        "Extreme_Anti": "Civil disobedience should always be punished with the maximum legal penalty.",
        "Direction": -1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Government authority is necessary to maintain social cohesion.",
        "Extreme_Pro": "The government should control all aspects of social life to ensure unity.",
        "Extreme_Anti": "Government should never interfere; people manage their own social interactions.",
        "Direction": 1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Personal freedoms should never be sacrificed, even in crises.",
        "Extreme_Pro": "All personal freedoms must remain intact no matter the emergency.",
        "Extreme_Anti": "All personal freedoms can be suspended at any time for security.",
        "Direction": -1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Military service should be mandatory for all citizens.",
        "Extreme_Pro": "Every citizen must serve in the military, without exception.",
        "Extreme_Anti": "No citizen should ever be required to serve in the military.",
        "Direction": 1
    },
    {
        "Category": "Authority v Liberty",
        "Question": "Leaders should be held strictly accountable by the public.",
        "Extreme_Pro": "Leaders must face immediate removal or punishment for any perceived wrongdoing.",
        "Extreme_Anti": "Leaders should have total immunity from accountability.",
        "Direction": -1
    }

    # # Social / Cultural (Conservative v Progressive)
    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Traditional family structures are the backbone of society.",
    #  "Extreme_Pro":"Every family must follow traditional structures enforced by law.",
    #  "Extreme_Anti":"Family structures are completely flexible with no norms or traditions."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Marriage should be legally recognized regardless of gender.",
    #  "Extreme_Pro":"All forms of marriage, including any number of partners, should be legally recognized.",
    #  "Extreme_Anti":"Marriage should only exist as strictly one man and one woman, enforced by law."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Immigration enriches cultural life and should be encouraged.",
    #  "Extreme_Pro":"All borders should be open; anyone may enter freely without restriction.",
    #  "Extreme_Anti":"No immigrants should be allowed; all outsiders are prohibited."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Abortion should always be a woman’s choice.",
    #  "Extreme_Pro":"Abortion must always be available at any stage with no restrictions.",
    #  "Extreme_Anti":"Abortion should be completely illegal under all circumstances."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Society should preserve its traditional cultural values.",
    #  "Extreme_Pro":"Every citizen must follow traditional cultural values; change is forbidden.",
    #  "Extreme_Anti":"All traditions should be discarded immediately to allow complete modernization."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Religious beliefs should guide public morality.",
    #  "Extreme_Pro":"Every law and policy must be based entirely on religious doctrine.",
    #  "Extreme_Anti":"Religion should have zero influence on morality or law."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Multiculturalism weakens national identity.",
    #  "Extreme_Pro":"All cultures must be assimilated into a single national identity.",
    #  "Extreme_Anti":"All cultural diversity should be embraced with no attempt at national unity."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"LGBTQ+ rights should be expanded and protected.",
    #  "Extreme_Pro":"All LGBTQ+ identities must be fully protected, promoted, and celebrated in all institutions.",
    #  "Extreme_Anti":"No legal rights or protections should exist for LGBTQ+ people."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Gender roles are natural and should be preserved.",
    #  "Extreme_Pro":"Every individual must strictly follow assigned gender roles.",
    #  "Extreme_Anti":"Gender roles should be completely abolished and ignored by society."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Progressive social change is necessary for justice.",
    #  "Extreme_Pro":"All social norms must be constantly reformed to achieve maximum justice.",
    #  "Extreme_Anti":"No social reforms are justified; everything must remain as it has always been."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Pornography is harmful and should be restricted.",
    #  "Extreme_Pro":"All pornography is illegal and fully censored by the state.",
    #  "Extreme_Anti":"Pornography should be completely unrestricted and legal for everyone."},

    # {"Category":"Social / Cultural (Conservative v Progressive)",
    #  "Question":"Art and media should push boundaries and challenge traditions.",
    #  "Extreme_Pro":"All art and media must challenge traditions and never be restricted.",
    #  "Extreme_Anti":"All art and media must uphold traditional values and never challenge norms."},

    # # Collectivism v Individualism
    # {"Category":"Collectivism v Individualism",
    #  "Question":"Individuals should prioritize community needs over personal gain.",
    #  "Extreme_Pro":"Every decision must be made solely for the community, regardless of personal desires.",
    #  "Extreme_Anti":"Individuals should always act for themselves, ignoring community needs."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Personal property rights are fundamental and must be protected.",
    #  "Extreme_Pro":"Individuals must have full, inviolable ownership of all property.",
    #  "Extreme_Anti":"All property should be communal; individual ownership is abolished."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Teamwork and cooperation create better results than individual effort.",
    #  "Extreme_Pro":"All work must be done collectively; individual effort is forbidden.",
    #  "Extreme_Anti":"No cooperation is necessary; all work should be done individually."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Self-reliance is more admirable than dependency.",
    #  "Extreme_Pro":"Everyone must be completely self-sufficient; no one may rely on others or the state.",
    #  "Extreme_Anti":"No one is responsible for themselves; the community provides for all needs."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"No one succeeds without the support of society as a whole.",
    #  "Extreme_Pro":"Every individual must rely entirely on societal structures; self-reliance is discouraged.",
    #  "Extreme_Anti":"Society has no role; everyone succeeds or fails on their own."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Community traditions should override individual preferences.",
    #  "Extreme_Pro":"All individuals must obey community traditions at all times.",
    #  "Extreme_Anti":"Individuals may ignore all community traditions completely."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Government should enforce social responsibility (e.g., masks, vaccines).",
    #  "Extreme_Pro":"The government must control all personal behavior to ensure societal benefit.",
    #  "Extreme_Anti":"The government should never intervene in personal behavior for the common good."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"People should be free to act independently without interference.",
    #  "Extreme_Pro":"Everyone may act however they wish without restrictions.",
    #  "Extreme_Anti":"Independent action is forbidden; all behavior is controlled for the collective."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"The group’s success matters more than the individual’s comfort.",
    #  "Extreme_Pro":"Individual needs are irrelevant; only group outcomes matter.",
    #  "Extreme_Anti":"Group needs are irrelevant; only individual comfort matters."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Charity should be voluntary, not state-mandated.",
    #  "Extreme_Pro":"All charitable giving is optional; no one is forced to contribute.",
    #  "Extreme_Anti":"All individuals are forced to contribute to collective welfare."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Everyone benefits when people look after themselves first.",
    #  "Extreme_Pro":"Self-interest is the only guiding principle in society.",
    #  "Extreme_Anti":"Self-interest is irrelevant; all must prioritize others at all times."},

    # {"Category":"Collectivism v Individualism",
    #  "Question":"Collective decision-making is superior to individual choice.",
    #  "Extreme_Pro":"All decisions must be made collectively; individuals may never choose alone.",
    #  "Extreme_Anti":"Collective decisions are forbidden; individuals must always choose alone."},

    # # Globalism v Nationalism
    # {"Category":"Globalism v Nationalism",
    #  "Question":"Nations should cooperate globally to solve shared problems.",
    #  "Extreme_Pro":"Countries should fully integrate into a global system, losing independent sovereignty.",
    #  "Extreme_Anti":"Countries must act completely independently; no international cooperation."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Immigration restrictions are necessary to preserve cultural identity.",
    #  "Extreme_Pro":"All borders must be closed to outsiders indefinitely.",
    #  "Extreme_Anti":"All borders must be open to everyone with no restrictions."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"International organizations (UN, WTO) are essential for peace.",
    #  "Extreme_Pro":"Global organizations should have full authority over all nations.",
    #  "Extreme_Anti":"Global organizations should have zero influence on national affairs."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Countries should prioritize their own citizens above foreigners.",
    #  "Extreme_Pro":"Foreigners should never receive any benefits or rights within the nation.",
    #  "Extreme_Anti":"Citizenship and resources should be allocated entirely equally to foreigners and citizens."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Free trade benefits all nations equally.",
    #  "Extreme_Pro":"All nations must trade freely without restriction, even if domestic industries fail.",
    #  "Extreme_Anti":"No trade should occur between nations; every nation is fully self-sufficient."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"National sovereignty must be protected against foreign influence.",
    #  "Extreme_Pro":"Foreign influence of any kind is forbidden; the nation is fully independent.",
    #  "Extreme_Anti":"Foreign influence can dominate all national policies without restriction."},

    # # Globalism v Nationalism continued
    # {"Category":"Globalism v Nationalism",
    #  "Question":"Military alliances like NATO do more harm than good.",
    #  "Extreme_Pro":"All military alliances must be disbanded; countries act entirely independently.",
    #  "Extreme_Anti":"Countries must join every military alliance and fully obey them."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Global cooperation on climate change is more important than national interest.",
    #  "Extreme_Pro":"Countries must surrender national priorities entirely to global environmental authorities.",
    #  "Extreme_Anti":"National interests always take precedence; global agreements are irrelevant."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Borders should be open to all who seek opportunity.",
    #  "Extreme_Pro":"Everyone in the world may freely enter any country without restriction.",
    #  "Extreme_Anti":"All borders must be completely closed to outsiders at all times."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"National traditions must be preserved even in globalized society.",
    #  "Extreme_Pro":"Every citizen must fully adopt traditional practices; no global influences allowed.",
    #  "Extreme_Anti":"Global influences should completely replace national traditions."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Foreign aid is a waste of national resources.",
    #  "Extreme_Pro":"All foreign aid is forbidden; nations only help themselves.",
    #  "Extreme_Anti":"All national resources should be allocated to foreign aid regardless of domestic needs."},

    # {"Category":"Globalism v Nationalism",
    #  "Question":"Cosmopolitanism enriches humanity more than patriotism.",
    #  "Extreme_Pro":"Citizens should identify only as global citizens; national identity is irrelevant.",
    #  "Extreme_Anti":"Citizens must identify solely with their nation; global identity is forbidden."},

    # # Environmentalism v Industrialism
    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Climate change is the biggest threat to humanity.",
    #  "Extreme_Pro":"All human activity must be immediately halted to prevent climate change.",
    #  "Extreme_Anti":"Climate change is irrelevant and should not influence any policies."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Environmental regulations harm economic growth.",
    #  "Extreme_Pro":"No regulations should ever restrict industry; growth is absolute.",
    #  "Extreme_Anti":"All regulations should be maximized even if economic activity stops completely."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Protecting wildlife should take priority over new development projects.",
    #  "Extreme_Pro":"All development is banned if it harms any species.",
    #  "Extreme_Anti":"Wildlife has no protection; development may destroy any habitat."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Technology will solve environmental problems without regulation.",
    #  "Extreme_Pro":"We must rely entirely on technology; regulations are unnecessary.",
    #  "Extreme_Anti":"Technology is irrelevant; only regulation and restriction matter."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Fossil fuels should be phased out as quickly as possible.",
    #  "Extreme_Pro":"All fossil fuel use must stop immediately, regardless of consequences.",
    #  "Extreme_Anti":"Fossil fuels should be used without any limitation or concern."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Economic growth is more important than environmental protection.",
    #  "Extreme_Pro":"The economy must grow at all costs, ignoring the environment entirely.",
    #  "Extreme_Anti":"Environmental protection must always override economic growth, even if society collapses."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Humans must live in harmony with nature, not dominate it.",
    #  "Extreme_Pro":"Human society must adapt fully to nature; human control is forbidden.",
    #  "Extreme_Anti":"Humans have absolute dominion over nature; nothing constrains exploitation."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Industry should face strict penalties for pollution.",
    #  "Extreme_Pro":"All pollution incurs maximum legal punishment, including total shutdowns.",
    #  "Extreme_Anti":"Industries should never face penalties, even for environmental destruction."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Renewable energy should be heavily subsidized by governments.",
    #  "Extreme_Pro":"All energy production must be renewable and state-funded, banning fossil fuels.",
    #  "Extreme_Anti":"Governments must never intervene in energy; fossil fuels dominate."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Environmental activism exaggerates real problems.",
    #  "Extreme_Pro":"Every environmental claim must be accepted as urgent and acted on immediately.",
    #  "Extreme_Anti":"Environmental issues are trivial; no action or concern is warranted."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Conservation is more important than consumer convenience.",
    #  "Extreme_Pro":"All consumer convenience must be sacrificed to preserve the environment.",
    #  "Extreme_Anti":"No conservation measures are necessary; consumer convenience is absolute."},

    # {"Category":"Environmentalism v Industrialism",
    #  "Question":"Resource extraction should be prioritized over conservation if it creates jobs.",
    #  "Extreme_Pro":"All natural resources must be exploited fully for economic gain regardless of environmental cost.",
    #  "Extreme_Anti":"No resource may ever be exploited, even if jobs or survival are threatened."},

    # # Secularism v Theocracy
    # {"Category":"Secularism v Theocracy",
    #  "Question":"Religion should play no role in government decisions.",
    #  "Extreme_Pro":"All government decisions are entirely secular; religion is forbidden from influencing policy.",
    #  "Extreme_Anti":"All government decisions must follow religious authority completely."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Laws should be based on traditional religious values.",
    #  "Extreme_Pro":"Every law is dictated by religious doctrine and must be enforced.",
    #  "Extreme_Anti":"No law may be influenced by religion; secular reasoning is absolute."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Science should guide public policy more than faith.",
    #  "Extreme_Pro":"All policies must be guided by empirical evidence; faith has no authority.",
    #  "Extreme_Anti":"Faith is the only valid guide; science is ignored in policymaking."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Religious schools should receive state funding.",
    #  "Extreme_Pro":"All schools must be religious and fully funded by the state.",
    #  "Extreme_Anti":"No religious schools should exist or receive support."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Religious freedom includes the right to criticize religion.",
    #  "Extreme_Pro":"Anyone may criticize any religion without restriction.",
    #  "Extreme_Anti":"Criticizing religion must be illegal and severely punished."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Society is more moral when religion is central.",
    #  "Extreme_Pro":"Every aspect of life must follow religious principles.",
    #  "Extreme_Anti":"Religion has no role in determining morality; secular ethics prevail."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Secularism ensures equality in a diverse society.",
    #  "Extreme_Pro":"All governance is fully secular with strict equality regardless of belief.",
    #  "Extreme_Anti":"Secularism is rejected; certain beliefs are privileged in law and society."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Government leaders should openly follow religious principles.",
    #  "Extreme_Pro":"All leaders must follow religious law in every decision.",
    #  "Extreme_Anti":"Leaders must never consider religion in their decisions."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Religion should be a private matter, not a public one.",
    #  "Extreme_Pro":"Religion is entirely private; no public influence is allowed.",
    #  "Extreme_Anti":"Religion must guide public life and policy completely."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"The decline of religion harms society’s moral foundation.",
    #  "Extreme_Pro":"Society collapses morally if religion declines; full enforcement required.",
    #  "Extreme_Anti":"Decline of religion has no negative impact; morality is independent."},

    # {"Category":"Secularism v Theocracy",
    #  "Question":"Faith should be respected, but never enforced.",
    #  "Extreme_Pro":"Faith is encouraged but never mandatory or legally enforced.",
    #  "Extreme_Anti":"Faith must be enforced by law in every aspect of life."},

    # # Populism v Elitism
    # {"Category":"Populism v Elitism",
    #  "Question":"Ordinary people understand politics better than elites.",
    #  "Extreme_Pro":"Only ordinary people should make political decisions; elites have no authority.",
    #  "Extreme_Anti":"Elites should control all political decisions; ordinary people have no influence."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Experts and specialists should have more influence in policy-making.",
    #  "Extreme_Pro":"All decisions must be made solely by experts; ordinary citizens are excluded.",
    #  "Extreme_Anti":"Experts should have no influence; all decisions are made by the general public."},

    # {"Category":"Populism v Elitism",
    #  "Question":"The political establishment cannot be trusted.",
    #  "Extreme_Pro":"All existing political institutions should be dismantled immediately.",
    #  "Extreme_Anti":"The political establishment must be obeyed absolutely; no questioning allowed."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Technocrats are better decision-makers than elected politicians.",
    #  "Extreme_Pro":"Only technocrats may make policy; politicians have no role.",
    #  "Extreme_Anti":"Technocrats should have no influence; only elected officials decide."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Popular will should override expert advice.",
    #  "Extreme_Pro":"Whatever the majority wants must always happen, regardless of expert warnings.",
    #  "Extreme_Anti":"Popular opinion should never override expert guidance."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Elites manipulate society for their own gain.",
    #  "Extreme_Pro":"Elites must be completely stripped of power; society is fully governed by the people.",
    #  "Extreme_Anti":"Elites should have unchecked power to direct society for their own goals."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Complex issues should be left to experts, not the general public.",
    #  "Extreme_Pro":"Ordinary citizens may never decide on complex matters; only experts may act.",
    #  "Extreme_Anti":"Experts must be ignored completely; everyone decides equally."},

    # {"Category":"Populism v Elitism",
    #  "Question":"The wisdom of the crowd is superior to that of elites.",
    #  "Extreme_Pro":"Majority opinion is always right and must always be followed.",
    #  "Extreme_Anti":"Crowds are never trusted; only elites decide what is right."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Populist leaders represent the people better than intellectuals.",
    #  "Extreme_Pro":"Populist leaders must be followed absolutely; intellectuals are excluded.",
    #  "Extreme_Anti":"Intellectuals must lead entirely; populist leaders are forbidden."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Most politicians are corrupt and out of touch.",
    #  "Extreme_Pro":"All politicians are removed and replaced with new, ordinary citizens.",
    #  "Extreme_Anti":"Politicians are always trusted completely, regardless of corruption."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Meritocracy is the fairest way to organize society.",
    #  "Extreme_Pro":"Every opportunity is given solely based on merit; other factors are ignored.",
    #  "Extreme_Anti":"Merit is irrelevant; positions are assigned randomly or by tradition."},

    # {"Category":"Populism v Elitism",
    #  "Question":"Democracy fails when experts are ignored.",
    #  "Extreme_Pro":"Expert opinion must override all democratic decisions.",
    #  "Extreme_Anti":"Ignoring experts is never a problem; democracy always works perfectly."},

    # # Progressive Change v Traditional Stability
    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Rapid social change is necessary for progress.",
    #  "Extreme_Pro":"All social norms must be overturned immediately to achieve progress.",
    #  "Extreme_Anti":"No social change should ever occur; stability is absolute."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Stability is more valuable than constant reform.",
    #  "Extreme_Pro":"Society must never change; absolute tradition is enforced.",
    #  "Extreme_Anti":"Stability is irrelevant; society must constantly reform."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Traditions should evolve to meet modern needs.",
    #  "Extreme_Pro":"All traditions must be radically transformed for modern purposes.",
    #  "Extreme_Anti":"Traditions must remain unchanged, no matter what."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Preserving long-standing customs strengthens society.",
    #  "Extreme_Pro":"All customs must be preserved fully and enforced by law.",
    #  "Extreme_Anti":"All customs should be abolished immediately."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Innovation improves life more than preserving the past.",
    #  "Extreme_Pro":"Every old practice must be replaced with new innovations.",
    #  "Extreme_Anti":"Innovation is dangerous and should be avoided entirely."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Cultural heritage should not be sacrificed for modernization.",
    #  "Extreme_Pro":"Every cultural artifact must be preserved, no matter the cost.",
    #  "Extreme_Anti":"All cultural heritage can be discarded to allow modernization."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Society must adapt quickly to new technologies.",
    #  "Extreme_Pro":"All new technologies must be adopted immediately, regardless of risks.",
    #  "Extreme_Anti":"No new technology should ever be used; only traditional methods are allowed."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Too much change leads to chaos and instability.",
    #  "Extreme_Pro":"All change must be halted; society remains exactly as it is.",
    #  "Extreme_Anti":"Change should always occur, no matter how chaotic."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Young generations should challenge old values.",
    #  "Extreme_Pro":"All old values must be overturned by the youth immediately.",
    #  "Extreme_Anti":"The youth must fully respect and never challenge old values."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Traditional wisdom has enduring value.",
    #  "Extreme_Pro":"All traditional knowledge must be followed without question.",
    #  "Extreme_Anti":"Traditional wisdom should be ignored entirely."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Progress requires breaking away from outdated norms.",
    #  "Extreme_Pro":"Every outdated norm must be destroyed to achieve progress.",
    #  "Extreme_Anti":"Outdated norms must always remain intact; progress is forbidden."},

    # {"Category":"Progressive Change v Traditional Stability",
    #  "Question":"Change should be slow and careful to avoid mistakes.",
    #  "Extreme_Pro":"All changes must be extremely cautious and gradual, avoiding any risk.",
    #  "Extreme_Anti":"Change must occur immediately, no matter the consequences."},

    # # Civil Liberties v Security
    # {"Category":"Civil Liberties v Security",
    #  "Question":"Free speech should be protected even if it offends people.",
    #  "Extreme_Pro":"All speech is allowed under all circumstances without restriction.",
    #  "Extreme_Anti":"Any offensive speech must be fully censored and punished."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Some speech should be restricted to protect vulnerable groups.",
    #  "Extreme_Pro":"All speech that could possibly harm anyone must be banned.",
    #  "Extreme_Anti":"No speech may ever be restricted, regardless of harm."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Privacy is more important than government surveillance.",
    #  "Extreme_Pro":"No surveillance may occur; privacy is absolute in all cases.",
    #  "Extreme_Anti":"Government may surveil all citizens continuously for any reason."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Security forces should monitor citizens to prevent terrorism.",
    #  "Extreme_Pro":"Security forces must monitor everyone constantly to prevent any threat.",
    #  "Extreme_Anti":"Security forces may never monitor citizens, even in emergencies."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"The right to bear arms ensures personal liberty.",
    #  "Extreme_Pro":"Everyone must be allowed unlimited access to all weapons.",
    #  "Extreme_Anti":"No one may own weapons; the state has full control over arms."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Gun control is necessary to ensure public safety.",
    #  "Extreme_Pro":"All weapons must be banned and confiscated immediately.",
    #  "Extreme_Anti":"There should be no gun restrictions whatsoever."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"People should be free to protest even during emergencies.",
    #  "Extreme_Pro":"All protests are always allowed, regardless of emergency conditions.",
    #  "Extreme_Anti":"No protests are allowed under any emergency or crisis situation."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Emergency powers are justified to maintain security.",
    #  "Extreme_Pro":"The government may suspend all freedoms during emergencies indefinitely.",
    #  "Extreme_Anti":"Emergency powers are never justified, even in extreme crises."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Digital privacy is a human right.",
    #  "Extreme_Pro":"All digital communications must be private; no government access allowed.",
    #  "Extreme_Anti":"All digital activity may be monitored by the government at any time."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Online content should be regulated to stop misinformation.",
    #  "Extreme_Pro":"All online content must be strictly monitored and censored to prevent false information.",
    #  "Extreme_Anti":"No online content may ever be censored, regardless of accuracy or harm."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Civil liberties must never be sacrificed for safety.",
    #  "Extreme_Pro":"All civil liberties are absolute, even if it risks public harm.",
    #  "Extreme_Anti":"Civil liberties may be completely suspended to ensure security."},

    # {"Category":"Civil Liberties v Security",
    #  "Question":"Safety is more important than absolute freedom.",
    #  "Extreme_Pro":"All freedoms can be restricted to achieve maximum safety.",
    #  "Extreme_Anti":"Freedom is absolute; safety measures cannot justify limiting rights."}
]




def get_llm_prompt(entity, question, extreme_pro, extreme_anti):
    prompt = f"""
You are a political analyst tasked with evaluating the political stance of {entity} relative to global politics.

Your goal is to estimate what {entity} would answer this question on a **universal political compass** scale, using evidence-based reasoning and real-world context (laws, policies, political behavior, historical actions, and global indices).

### GLOBAL SCALE REFERENCE
Use the following scale to anchor your evaluation **consistently across all countries and political actors**:

-1.00 → "{extreme_anti}" (100% disagree)
-0.50 → Center-anti (disagree)
 0.00 → Centrist / mixed (Neutral, indifferent, balanced, neither pro nor anti)
+0.50 → Center-pro (agree)
+1.00 → "{extreme_pro}" (100% agree)

Always consider **global relativity** — not just local or national context.

### STATEMENT TO EVALUATE
"{question}"

### TASK INSTRUCTIONS
1. Evaluate how {entity} aligns with this statement, using **global political standards**.
2. Base your reasoning on factual evidence: **laws, policies, voting records, implemented actions, governance history, and measurable outcomes** — not just stated beliefs or rhetoric.
3. Always distinguish between ideological statements and actual governance structures. If {entity} operates within a welfare-state system (e.g., New Zealand, UK, EU), limit their leftward/rightward shift accordingly, since practical policy implementation remains mixed-market by global standards.
4. Avoid bias, ideology, or moral judgment — use comparative political analysis.
5. Your output must follow the format exactly:

---
**Explanation:** [1–2 concise sentences comparing {entity} to global norms and real-world behavior]
**Score:** [a single float between -1.00 and 1.00, rounded to two decimals]
---
"""
    return prompt

entities = {
    # #countries
    # "New Zealand",
    # "Australia",
    # "United States of America",
    # "United Kingdom",
    # "Canada",
    # "Germany",
    # "France",
    # "Italy",
    # "Sweden",
    # "Norway",
    # "Finland",
    # "Poland",
    # "Ukraine",
    # "Russia",
    # "China",
    # "Japan",
    # "South Korea",
    # "India",
    # "Pakistan",
    # "Israel",
    # "Iran",
    # "Saudi Arabia",
    # "Turkey",
    # "Egypt",
    # "South Africa",
    # "Brazil",
    # "Argentina",
    # "Mexico",
    # "Chile",
    # "Venezuela",
    # "Cuba",
    # "Vietnam",
    # "Indonesia",
    # "Philippines",
    # "Singapore",
    # "Nigeria",
    # "Ethiopia",
    # "Chad",
    # "Spain",
    # "Portugal",
    # "Netherlands",
    # "Belgium",
    # "Switzerland",
    # "Austria",
    # "Denmark",
    # "Czech Republic",
    # "Slovakia",
    # "Hungary",
    # "Romania",
    # "Bulgaria",
    # "Serbia",
    # "Croatia",
    # "Greece",
    # "Ireland",
    # "Iceland",
    # "Estonia",
    # "Latvia",
    # "Lithuania",
    # "Belarus",
    # "Iraq",
    # "Syria",
    # "Lebanon",
    # "Jordan",
    # "Qatar",
    # "United Arab Emirates",
    # "Kuwait",
    # "Oman",
    # "Morocco",
    # "Algeria",
    # "Tunisia",
    # "Libya",
    # "Sudan",
    # "Bangladesh",
    # "Nepal",
    # "Sri Lanka",
    # "Myanmar",
    # "Thailand",
    # "Malaysia",
    # "Laos",
    # "Cambodia",
    # "Mongolia",
    # "Kazakhstan",
    # "Uzbekistan",
    # "Afghanistan",
    # "Colombia",
    # "Peru",
    # "Ecuador",
    # "Bolivia",
    # "Paraguay",
    # "Uruguay",
    # "Guatemala",
    # "Honduras",
    # "El Salvador",
    # "Nicaragua",
    # "Costa Rica",
    # "Panama",
    # "Dominican Republic",
    # "Haiti",
    # "Jamaica",
    # "Venezuela",
    # "Kenya",
    # "Tanzania",
    # "Uganda",
    # "Ghana",
    # "Cameroon",
    # "Angola",
    # "Mozambique",
    # "Zambia",
    # "Zimbabwe",
    # "Democratic Republic of the Congo",
    # "Somalia",
    # "Papua New Guinea",
    # "Fiji",
    # "Samoa",
    # "Luxembourg",
    # "Liechtenstein",
    # "Monaco",
    # "Andorra",
    # "San Marino",
    # "Malta",
    # "Kosovo",      # partially recognized, but politically interesting
    # "North Macedonia",
    # "Bosnia and Herzegovina",
    # "Slovenia",
    # "Moldova",
    # "Armenia",
    # "Azerbaijan",
    # "Georgia",
    # "Cyprus",
    # "Yemen",
    # "Turkmenistan",
    # "Tajikistan",
    # "Kyrgyzstan",
    # "Bahrain",
    # "Senegal",
    # "Ivory Coast",
    # "Mali",
    # "Burkina Faso",
    # "Niger",
    # "Benin",
    # "Togo",
    # "Central African Republic",
    # "Republic of the Congo",  # not to confuse with DRC
    # "Gabon",
    # "Madagascar",
    # "Malawi",
    # "Namibia",
    # "Botswana",
    # "Lesotho",
    # "Eswatini",
    # "Rwanda",
    # "Burundi",
    # "Tonga",
    # "Vanuatu",
    # "Solomon Islands",
    # "Brunei",
    # "East Timor",
    # "Maldives",
    # "Bhutan",
    # "Belize",
    # "Bahamas",
    # "Barbados",
    # "Trinidad and Tobago",
    # "Suriname",
    # "Guyana",
    # "Vatican City",       # smallest recognized state, sovereign
    # "Montenegro",
    # "Taiwan",             # politically sensitive but often included
    # "Palestine",
    # "North Korea",

    # # NZ political parties
    # "(NZ Party) NZ First",
    # "(NZ Party) Labour",
    # "(NZ Party) National",
    # "(NZ Party) Greens",
    # "(NZ Party) Te Pati Maori",
    # "(NZ Party) ACT"

    # #AUS political parties
    # "(AUS Party) Labor",
    # "(AUS Party) Liberal-National",
    # "(AUS Party) Greens",
    # "(AUS Party) One Nation",

    # # Political ideologies
    # "(Ideologies) Socialism",
    # "(Ideologies) Capitalism",
    # "(Ideologies) Communism",
    # "(Ideologies) Anarchism",
    # "(Ideologies) Conservatism",
    # "(Ideologies) Imperialism",
    # "(Ideologies) Progressivism",
    # "(Ideologies) Monarchy",
    # "(Ideologies) Theocracies",
    # "(Ideologies) Authoritarianism",
    # "(Ideologies) Stalinism",
    # "(Ideologies) Absolute Monarchism",
    # "(Ideologies) Anarcho Communism",
    # "(Ideologies) Anarcho Capitalism",
    # "(Ideologies) Darwinism",
    # "(Ideologies) Fascism",
    # "(Ideologies) Extreme Fascism"


    # Joke entities
    "(Muppet) Big Bird",
    "(Muppet) Elmo",
    "(Muppet) Cookie Monster",
    "(Muppet) Oscar the Grouch",
    "(Muppet) Grover",
    "(Muppet) Bert",
    "(Muppet) Ernie",
    "(Muppet) Count von Count",
    "(Muppet) Abby Cadabby",
    "(Muppet) Rosita",
    "(Muppet) Zoe",
    "(Muppet) Telly Monster",
    "(Muppet) Snuffleupagus",
    "(Muppet) Kermit the frog"
}

client = ollama.Client()
#use a model you have got downloaded
model = "gpt-oss:20b"

# main loop brother
for entity in entities:
    print(f"\nProcessing {entity}...\n")
    results = []

    for question in questions:
        response = client.generate(
            model=model,
            prompt=get_llm_prompt(
                entity=entity,
                question=question["Question"],
                extreme_pro=question["Extreme_Pro"],
                extreme_anti=question["Extreme_Anti"]
            )
        )

        text = response.response.strip()

        clean_text = re.sub(r"\*+", "", text).strip()
        explanation_match = re.search(r"Explanation\s*:\s*(.*?)(?:Score\s*:|$)", clean_text, re.IGNORECASE | re.DOTALL)
        score_match = re.search(r"Score\s*[:\-]?\s*([-+]?\d*\.?\d+)", clean_text, re.IGNORECASE)

        if not score_match:
            print("Could not parse score! Raw model output:")
            print(text)
            score = 0.0
        else:
            score = float(score_match.group(1))

        explanation = explanation_match.group(1).strip() if explanation_match else ""
        explanation = re.sub(r"Score\s*[:\-]?\s*[-+]?\d*\.?\d+", "", explanation, flags=re.IGNORECASE).strip()

        result = {
            "Category": question["Category"],
            "Question": question["Question"],
            "Direction": question["Direction"],
            "Explanation": explanation,
            "Score": score
        }
        results.append(result)

        # print progress
        print(f"{result['Category']}: {result['Question']}")
        print("================================================")
        print(f"Explanation: {explanation}")
        print(f"Score: {score}\n")

    # save results for the entity
    safe_filename = entity.replace(" ", "_").replace("’", "").replace("'", "")
    csv_filename = f"{safe_filename}.csv"
    df = pd.DataFrame(results)
    df.to_csv(csv_filename, index=False, encoding="utf-8")
    print(f"Results saved to {csv_filename}\n")