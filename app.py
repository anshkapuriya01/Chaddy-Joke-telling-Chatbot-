from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# A curated list of Dark Humor & College Life jokes in Hinglish.
# Longer, clearer, and darker as requested.
all_jokes = [
    # --- Dark Life & Existential Dread ---
    "Maine Suicide Helpline pe call kiya, unhone pucha 'Kya pareshani hai?', maine bola 'Balance khatam ho gaya hai'. Unhone call kaat diya. Shayad wo bhi samajh gaye. 😂",
    "Doctor ne bola 'Aapki report positive hai', maine khushi se pucha 'Corona?', wo bola 'Nahi, HIV. At least life mein kuch toh positive hai'. 😂",
    "Zindagi aur maut mein bas saanso ka farak hai, aur meri saansein bhi ab 'Low Battery' notification de rahi hain. 😂",
    "Log kehte hain 'Marne ke baad sab theek ho jayega', toh main soch raha hoon aaj hi trial run le lun. 😂",
    "Mere guardian angel ne mujhe dekh kar suicide kar liya, letter mein likha tha 'Isse bachana mere syllabus ke bahar hai'. 😂",
    "Yamraj aaye the lene, maine bola 'EMI pending hai', toh wo bole 'Koi nahi, main wait kar leta hoon, bank wale zyada khatarnak hain'. 😂",
    "Agar main mar gaya toh meri asthiyan waheen baha dena jahan se meri crush guzarti hai, kam se kam wo mujhe chu toh legi. 😂",
    "Main itna akela hoon ki agar main kidnap ho gaya, toh kidnappers mujhe wapas chhod jayenge kyunki unhe mere rone se sar dard ho jayega. 😂",
    "Zindagi ne mujhe 'Lemon' nahi diye, seedha aankh mein acid daala hai, aur main ab andha hokar bhi pretend kar raha hoon ki sab dikh raha hai. 😂",
    "Mera future itna dark hai ki black hole bhi mujhe dekh kar Sharma jaye aur bole 'Bhai, thoda light jala le'. 😂",
    "Log bolte hain 'Khush raho', jaise khushi Amazon pe order karke agle din delivery mil jayegi. 😂",
    "Mere funeral pe please 'Happy Birthday' bajana, taaki logon ko confuse kar sakun ki main paida hua tha ya marne aaya tha. 😂",
    "Agar maut ek aurat hoti, toh main usse shadi kar leta, kam se kam wo mujhe kabhi dhoka toh nahi deti... wo toh aani hi hai. 😂",
    "Bachpan mein andhere se darr lagta tha, ab light on karne se lagta hai kyunki bijli ka bill aur shakal dono darawani hai. 😂",
    "Maine mirror mein dekh kar bola 'I love you', mirror toot gaya. Ab samajh nahi aa raha 7 saal ka bad luck hai ya mirror ne suicide kiya. 😂",
    "Bhagwan ne mujhe bheja toh hai dharti pe, lekin lagta hai 'Return Policy' expired thi isliye wapas nahi le rahe. 😂",
    "Log kehte hain 'Paisa haath ka mail hai', toh main shayad duniya ka sabse hygienic insaan hoon, haath ekdum saaf rehte hain. 😂",
    "Meri kismat us machhar jaisi hai jo khoon peene aata hai par galti se 'All Out' machine par baith jata hai. 😂",
    "Duniya mein do tarah ke log hote hain: Ek jo jeene ke liye khate hain, aur ek main, jo maut ka intezaar karte hue snacks kha raha hoon. 😂",
    "Agar depression ek sport hota, toh main aaj Olympic Gold Medalist hota aur desh ka naam roshan karta... ya shayad tab bhi 4th aata. 😂",
    "Main chahta hoon log mujhe mere kaam se jaane... par afsos, main toh berozgaar hoon. 😂",
    "Zindagi mein sabse bada motivation tab milta hai jab phone ki battery 1% ho aur charger doosre kamre mein ho. Wahi asli 'Survival Instinct' hai. 😂",
    "Maine pucha 'Siri, main single kyun hoon?', Siri ne front camera on kiya aur boli 'Khud dekh le bhai, explanation ki zaroorat nahi'. 😂",
    "Log kehte hain 'Dil ki suno', mera dil toh bas 'Lup-Dup' karta hai, ismein se kaunsi language decode karun? 😂",
    "Mera bank account balance dekh ke ATM machine ne screen pe 'LOL' likh diya, cash ki jagah tissue paper bahar aaya. 😂",
    "Rishtedar puchte hain 'Beta aage ka kya plan hai?', maine bola 'Bas saans rukne ka wait kar raha hoon, uske baad plan hi plan hai'. 😂",
    "Agar main Titanic pe hota, toh iceberg se takrane se pehle hi main paani mein kood jata, kyunki meri kismat mein toh doobna hi likha hai. 😂",
    "Psychologist ne bola 'Write a letter to the people you hate and burn it'. Maine kiya, ab wo puch raha hai 'Unn logon ki body ka kya karun?'. 😂",
    "Maut aani hai ye tay hai, par ye Monday har hafte kyun aa jata hai? Iska subscription cancel kaise karun? 😂",
    "Main itna negative hoon ki agar main photo develop karne jaun dark room mein, toh wo photo bhi blank aayegi. 😂",
    "Shadi kar lo, taaki do log milke ek dusre ki zindagi systematically barbad kar sakein, akele suffer karne mein wo maza kahan. 😂",
    "Mere paas Plan B nahi hai, kyunki Plan A bhi bas 'Dekha jayega, jo hoga wo jhela jayega' tha. 😂",
    "Agar main billi hota toh 9 lives hoti, yahan ek life bhi dhang se nahi chal rahi, upar se 8 aur jhelni padti? No thanks. 😂",
    "Mere mood swings dekh ke park ke jhule bhi sharma jayein, unhe lagta hai wo tez ghoomte hain. 😂",
    "Zindagi ek puzzle hai, aur main wo piece hoon jo box mein aaya hi nahi, ya shayad kisi ne galti se vacuum cleaner mein kheench liya. 😂",
    "Bhagwan ne mujhe banaya aur phir template delete kar diya taaki galti repeat na ho. Ek hi masterpiece (ya disaster) kaafi hai. 😂",
    "Main crowd mein isliye khada hota hoon taaki sniper confuse ho jaye aur galti se kisi aur ko uda de. Survival tactics! 😂",
    "Success mere peeche bhaag rahi thi, par main usse tez bhaag gaya. Maine socha police hai. 😂",
    "Dukh batne se kam hota hai? Maine try kiya, saamne wala bhi rone laga meri halat dekh ke. Ab hum dono depressed hain. 😂",
    "Bas saans chal rahi hai, baaki toh system hang hai. Task Manager bhi 'Not Responding' dikha raha hai. 😂",
    "Duniya gol hai, par meri kismat seedhi khaayi mein ja rahi hai, bina kisi turning point ke. 😂",
    "Log kehte hain 'Time heals everything', par time ke paas medical degree hai kya? Ya wo bhi jhola chhaap doctor hai? 😂",
    "Mera talent hai galat waqt pe galat decision lena, aur main ismein PhD kar chuka hoon. 😂",
    "Khushi bas ek afwah hai, jo Instagram pe failayi gayi hai taaki hum jaise log bura feel karein. 😂",
    "Meri kismat 'Error 404' hai, kabhi milti hi nahi. Server hi down rehta hai hamesha. 😂",
    "Bachpan mein mummy bolti thi 'Soja warna bhoot aayega', ab bhoot bhi bolta hai 'Soja warna depression aayega, aur wo mujhse zyada darawana hai'. 😂",
    "Interview mein poocha 'Under pressure kaam kar sakte ho?', maine kaha 'Main toh saans bhi pressure mein leta hoon, mera blood group hi BP+ hai'. 😂",
    "Socha tha gym jaake body banaunga, phir yaad aaya laash toh waise bhi jalani hi hai, 6-pack abs ka kya achar dalunga? 😂",
    "Log kehte hain 'Khali haath aaye the, khali haath jayenge', par main toh karza leke jaunga, bank walon ko dhoka dene ka maza hi kuch aur hai. 😂",
    "Meri life ki movie flop ho gayi kyunki script writer nashadi tha aur director ne beech mein hi give up kar diya. 😂",
    "Mera bank mujhe loan offer nahi karta, seedha bhikhariyon ki scheme bhejta hai aur bolta hai 'Try this, better chances'. 😂",
    "Rishtedaar bolte hain 'Tumhare chehre pe raunak nahi hai', ab unhe kaise bataun ye 'Dead inside' look hai, jo abhi trending hai. 😂",
    "Shaitan bhi meri paap ki list dekh ke bolta hai, 'Bhai, tu toh legend nikla, main toh bas internship kar raha tha'. 😂",
    "Zindagi mein do hi cheezein constant hain: Mera bad luck aur doston ki udhaari jo wo kabhi wapas nahi karte. 😂",
    "Mujhe 'Headache' nahi hota, mera pura existence hi ek headache hai, bas sar dard hona band ho gaya hai kyunki aadat ho gayi hai. 😂",
    "Log bolte hain 'Think Positive', maine socha main crorepati hoon, bank ne bola 'Rehne do, sapne mein bhi balance negative hai'. 😂",
    "Maut toh ek bahana hai, asli maksad toh office se permanent chutti lena hai bina notice period serve kiye. 😂",
    "Mere dimaag mein 'Delete' button nahi hai, bas 'Overthink' ka infinite loop hai jo raat ke 3 baje chalta hai. 😂",
    "Bhoot mere sapne mein aaya, maine bola 'Rent dega toh ruk, warna nikal'. Wo dar ke maare bhaag gaya. 😂",
    "Meri love life aur Bermuda Triangle same hain, jo jaata hai gayab ho jata hai, aur kabhi wapas nahi aata. 😂",
    "Agar 'Disappointment' ka koi chehra hota, toh wo mera Passport photo hota, jise dekh ke immigration officer bhi taras khaata hai. 😂",
    "Yamraj ne mujhe reject kar diya, bole 'Iska quota abhi poora nahi hua suffering ka, isse aur tadpao dharti pe'. 😂",
    "Log 'Future planning' karte hain, main bas 'Dinner planning' tak soch paata hoon, uske aage sab dhundhla hai. 😂",
    "Mera talent hai sahi mauke pe galat baat bolna aur phir regret karna jab tak neend na aaye. 😂",
    "Zindagi ne mujhe 'Lemon' nahi diye, seedha aankh mein acid daala hai taaki main dekh na sakun ki meri life kitni kharab hai. 😂",
    "Main khush hone ki acting itni achi karta hoon, Oscar wale confuse hain ki mujhe award dein ya mental hospital bhejein. 😂",
    "Doctor ne bola 'Stress mat lo', ab use kaun bataye stress hi meri oxygen hai, bina tension ke main saans kaise lun? 😂",
    "Phone ki brightness kam rakhta hoon, taaki meri future ki tarah dark match kare, consistency is key. 😂",
    "Har subah uth ke lagta hai, 'Yaar, phir se wahi survival game shuru, save point kahan hai is game ka?'. 😂",
    "Main apne problems ko ignore karta hoon, jaise ladkiyan mujhe karti hain. Perfect symmetry! 😂",
    "Agar aasun bech sakte, toh main aaj Ambani se ameer hota, mera startup unicorn ban chuka hota. 😂",
    "Zindagi ek race hai, aur main spectator stand mein baitha hoon popcorn khaate hue, dekhte hue ki baaki log kaise gir rahe hain. 😂",
    "Mujhe lagta hai bhagwan ne meri kundali Excel sheet pe banayi thi aur file corrupt ho gayi, ab data recover nahi ho raha. 😂",
    "Log kehte hain 'Hard work pays off', mera waala shayad cheque bounce ho gaya ya sign match nahi hua. 😂",
    "Main itna aalsi hoon ki agar maut aayi, toh bolunga 'Kal aana, aaj mood nahi hai marne ka'. 😂",
    "Mera dimaag 90% song lyrics aur 10% regret se bana hai, padhai ka data toh corrupt ho gaya. 😂",
    "Gareebi darwaze pe aayi toh maine bola 'Bhai, tu late hai, depression pehle se sofa pe baitha hai, jagah nahi hai'. 😂",
    "Agar main horror movie mein hota, toh main wo banda hota jo pehle scene mein hi mar jata hai taaki movie jaldi khatam ho aur main ghar ja sakun. 😂",
    "Log puchte hain 'Nashaa karte ho?', maine kaha 'Haan, ummeed ka... aur wo har baar tootta hai, phir bhi main addiction nahi chodta'. 😂",
    "Mera guardian angel cigarette break pe gaya tha, 20 saal se wapas nahi aaya. Lagta hai use cancer ho gaya. 😂",
    "Main chahta hoon log mujhe yaad rakhein... udhaar na chukane ke liye hi sahi, kam se kam yaad toh karenge. 😂",
    "Shadi mein log 'Lifelong happiness' wish karte hain, mujhe toh ye sarcasm lagta hai, jaise wo bol rahe hon 'Welcome to hell'. 😂",
    "Agar tension lene ke paise milte, toh main duniya ka sabse ameer aadmi hota, Elon Musk meri car drive karta. 😂",
    "Mera confidence level 'I agree' terms and conditions padhne jitna fake hai, bas tick kar deta hoon bina padhe. 😂",
    "Zindagi ne mujhe strong banaya hai... ya shayad bas numb kar diya hai, ab dard hi nahi hota, bas hassi aati hai. 😂",
    "Main swimming isliye nahi seekhta, kyunki doobna meri kismat mein likha hai, toh koshish kyun karun? 😂",
    "Log kehte hain 'Paisa bolta hai', mera waala bas 'Bye' bolke chala jata hai, kabhi 'Hi' bhi nahi bolta. 😂",
    "Main marne se nahi darta, bas dobara paida hone se darta hoon. Ek baar ka trauma hi kaafi hai. 😂",
    "Meri life mein 'Ups and Downs' nahi hain, bas 'Downs and Undergrounds' hain. Main patal lok ki taraf ja raha hoon. 😂",
    "Duniya ko bachana Superman ka kaam hai, mera kaam bas subah uth ke bed se nikalna hai, wahi mera daily mission hai. 😂",
    "Main itna single hoon ki ab phone company wale bhi 'I love you' bolne lage hain offer dene ke liye, unhe bhi taras aa gaya hai. 😂",
    "Ant mein sab theek ho jata hai... agar theek nahi hua, toh samjho ant abhi hua nahi... ya fir tumhari kismat hi kharab hai, jo ki most likely hai. 😂",
    "Log kehte hain 'Jaan hai toh jahan hai', meri toh jaan hi aafat mein hai, toh jahan ka main kya achar dalun? 😂",

    # --- Dark College & Student Life (Longer & Clearer) ---
    "Assignment ki deadline mere sar pe aisi mandra rahi hai jaise Yamraj ki talwar, aur main yahan baith ke meme scroll kar raha hoon jaise main amar hoon. 😂",
    "Viva mein teacher ne poocha 'Zindagi ka maqsad kya hai?', maine rote hue bola 'Sir, bas ye subject pass kar do, baaki main Himalaya chala jaunga sanyas lene'. 😂",
    "Engineering karke bas ek hi skill seekhi hai maine: Bina ek shabd padhe poora exam kaise likhna hai aur phir bhi umeed rakhna ki pass ho jaunga. 😂",
    "Hostel ka khana kha ke ab mera immune system itna strong ho gaya hai ki zeher bhi pee lun toh body use 'Protein Shake' samajh ke digest kar legi. 😂",
    "Meri Degree deewar pe tangi hai aur main berozgaari ki lambi line mein khada hoon. Degree dekh ke lagta hai, isse acha toh tissue paper hi le leta, kam se kam rone ke kaam aata. 😂",
    "Placement cell wale bolte hain 'Bright Future', par mujhe toh tunnel mein bhi andhera dikh raha hai. Lagta hai future mein light ka bill nahi bhara kisi ne. 😂",
    "College ki canteen mein meri udhaari aur meri zindagi ki pareshani, dono compound interest ke saath badh rahi hain aur khatam hone ka naam nahi le rahi. 😂",
    "Attendance 75% chahiye college walon ko, par meri jeene ki iccha 0% ho gayi hai uska kya? Attendance poori karke bhi laash hi class mein baithegi na. 😂",
    "Exam hall mein ghuste hi dimaag 'Airplane Mode' pe chala jata hai. Wi-Fi signal toh door, basic memory bhi connect nahi hoti. 😂",
    "Syllabus itna vast hai ki lagta hai poora samandar peena hai, aur bhagwan ne mujhe dimaag ki jagah ek chammach diya hai wo bhi ched wala. 😂",
    "Roommate ke kharrate sun ke lagta hai main runway pe so raha hoon aur Boeing 747 mere kaan ke bagal se take-off kar raha hai har 5 second mein. 😂",
    "Library mein neend sabse achi aati hai, shayad kitabein lori gati hain ki 'Soja beta, padh ke bhi kya ukhaad lega, waise bhi berozgaar rehna hai'. 😂",
    "Professors ko lagta hai humein padhai se pyaar hai aur hum knowledge ke liye aate hain. Unhe kaun bataye hum bas degree ke liye aate hain taaki dahej ka rate badh sake. 😂",
    "Backlog clear karte karte, meri jawani clear ho gayi. Ab lagta hai degree ke saath mujhe senior citizen card bhi milega. 😂",
    "Mera CGPA aur mera cholesterol, dono badhne ka naam nahi le rahe. Dono ek constant low level pe maintain hain jo meri health aur career dono ke liye khatarnak hai. 😂",
    "Engineering ek tapasya hai, jisme fal ki chinta nahi karni chahiye, bas 'Pass' hone ki bheek maangi jaati hai har semester ke end mein. 😂",
    "Medical student hoon, khud ki body chod ke sabki body ke baare mein padh liya. Ab khud bimar padta hoon toh Google search karta hoon ki main marne wala hoon ya nahi. 😂",
    "MBA kar raha hoon, taaki suit pehen ke depression mein jaun. Kam se kam sadkone mein professional lagunga, bhale hi andar se khokhla hoon. 😂",
    "College fest mein maze karne gaye the, socha tha ladkiyan impress karenge. Wahan bhi volunteer banke kursi utha rahe the aur seniors ki gaaliyaan kha rahe the. 😂",
    "Group project ka matlab: Ek gadha kaam karega, baaki sab credit lenge aur teacher ke saamne aise act karenge jaise unhone hi rocket launch kiya hai. 😂",
    "Teacher ne gusse mein bola 'Get out of my class', maine man mein bola 'Thank God, azadi mili is torture chamber se'. Bahar jaake chain ki saans li. 😂",
    "Result wale din rishtedaron ke phone aise aate hain jaise unhone hi meri fees bhari ho. Unka bas chale toh wo mere marksheet ka printout nikal ke pure sheher mein baat dein. 😂",
    "Zindagi mein 2 cheezein mujhe aaj tak samajh nahi aayi: Engineering ki Engineering Drawing aur Ladki ki mood swings. Dono hi logic ke pare hain. 😂",
    "Internship mein stipend itna kam hai ki aane-jaane ka kiraya bhi ghar se maangna padta hai. Basically, main kaam karne ke liye paise de raha hoon. 😂",
    "College life 'Student of the Year' jaisi hogi socha tha, yahan toh 'Crime Patrol' chal raha hai. Har din ek naya hadsa, har din ek nayi maut (umeedon ki). 😂",
    "Assignment copy karte waqt handwriting change karna bhi ek art hai, jo har engineer ko seekhna padta hai. Hum content copy karte hain, par style apna rakhte hain. 😂",
    "External examiner shaitan ka doosra roop hota hai. Wo aise sawal puchta hai jo shayad usne khud bhi pehli baar sune honge, bas humein zaleel karne ke liye. 😂",
    "Fees bharne ke baad jo account mein bachta hai, usse 'chillar' bhi nahi kehte. Usse bas 'rounding error' kehte hain jo bank wale bhi ignore kar dete hain. 😂",
    "Raat bhar padhai ki, subah question paper dekh ke laga galti se doosre branch ka paper pakda diya hai. Syllabus toh match hi nahi ho raha tha. 😂",
    "HOD ke office ke bahar khade rehna, mandir ki line mein lagne se zyada mushkil hai. Mandir mein bhagwan sun bhi lete hain, HOD toh sunta hi nahi. 😂",
    "Class mein dhyan dene ki koshish karta hoon, toh neend mujhe apni baahon mein le leti hai. Lecture hall mein sleeping gas release hoti hai, pakka. 😂",
    "Practical file poori karna, Mahabharat likhne se kam nahi hai. Haath toot jate hain, par teacher ka 'Red Pen' kabhi satisfy nahi hota. 😂",
    "College ke dost saanp nahi, anaconda hote hain. Wo tab tak dost rehte hain jab tak assignment copy karna ho, uske baad 'Tu kaun, main kaun'. 😂",
    "Proxy lagwana dosti ka sabse bada saboot hai. Jo dost tumhari proxy lagaye, wahi asli bhai hai, baaki sab moh maya hai. 😂",
    "Mera dimaag exam mein bas ek hi cheez karta hai: 'Ye gaana suna hai?'. Poora playlist bajta hai dimaag mein, bas answer yaad nahi aata. 😂",
    "Topper ko rota dekh ke dil ko jo sukoon milta hai, wo Jannat hai. Lagta hai insaaf abhi zinda hai is duniya mein. 😂",
    "Result dekh ke papa ne bola 'Beta, tu rehne de, tere bas ka nahi hai', dil toot gaya par ek relief bhi mila ki ab umeed nahi rakhenge. 😂",
    "Degree lene stage pe gaya toh laga, 'Is ek kagaz ke tukde ke liye itna zaleel hua main 4 saal? Isse acha toh pakode bech leta'. 😂",
    "College bus mein seat milna, lottery lagne ke barabar hai. Jo seat milti hai wo singhasan se kam nahi lagti us waqt. 😂",
    "Lecture ke beech mein washroom jana, prison break jaisa lagta hai. Teacher ki permission lena matalb border cross karne ki permission lena. 😂",
    "Breakup ka dard teacher ke 'Surprise Test' se kam hota hai. Breakup mein dil toot-ta hai, surprise test mein future toot jata hai. 😂",
    "Hostel mein Maggie bana ke khana hi 'Fine Dining' hai. Usmein agar anda dal gaya toh wo 5-star hotel se kam nahi lagta. 😂",
    "Warden ko lagta hai hum chor hain, aur humein lagta hai wo jailor hai. Hostel nahi, Tihar Jail ka branch lagta hai kabhi kabhi. 😂",
    "College ke baad 'Scope' dhoondne nikla tha, ab telescope se bhi nahi dikh raha. Lagta hai scope zameen ke neeche dafn ho gaya hai. 😂",
    "Fresher party mein socha tha cool banunga aur impress karunga, senior banke ab khud depress hoon aur freshers ko dekh ke sochta hoon 'Bechare, inka katne wala hai'. 😂",
    "Engineering drawing ki sheet pe aansu girne se sheet kharab ho gayi, meri zindagi toh pehle se hi kharab thi, ab sheet bhi gayi. 😂",
    "Maths ke lecture mein 'Let x be...' sunte hi neend aa jati hai. Mujhe kya pata X kya hai, meri X toh chhod ke chali gayi. 😂",
    "Placement interview mein HR ne pucha 'What are your strengths?', maine bola 'Gham chupana aur fake smile karna'. Usne mujhe reject kar diya. 😂",
    "Corporate majdoor banne ki training college mein hi shuru ho jati hai. Assignment deadllines bas humein stress handle karna sikhate hain, knowledge nahi. 😂",
    "Ragging nahi hoti ab, bas 'Introduction' ke naam pe bezzati hoti hai. Seniors maze lete hain aur hum 'Sir, Sir' bolke izzat bachate hain. 😂",
    "College gate ke bahar ki chai hi asli energy drink hai. Wo gandi si chai peeke hi hum zinda hain, warna toh kab ke mar gaye hote. 😂",
    "Semester break ka wait karte karte semester khatam ho jata hai, aur break mein agle semester ki tension shuru ho jati hai. Chain kahan hai? 😂",
    "Online classes mein camera off karke web series dekhna hi asli talent hai. Teacher padha raha hai, aur hum Netflix and Chill kar rahe hain. 😂",
    "Zoom call pe 'Am I audible?' bolna, meri zindagi ka theme song ban gaya hai. Koi sun nahi raha, bas main bole ja raha hoon. 😂",
    "Assignment upload karne ke baad jo 'Submitted' likha aata hai, wo sukoon duniya ki kisi bhi cheez se badhkar hai. Lagta hai jung jeet li. 😂",
    "Degree mili, par dimaag wahin college canteen mein reh gaya. Ab body corporate mein hai aur aatma college ke momos wale ke paas. 😂",
    "Convocation gown pehen ke laga Harry Potter hoon, par jadoo toh unemployment ka hua. Job gayab ho gayi, bas loan reh gaya. 😂",
    "Alumni meet mein jaana hi nahi hai, wahan sab package discuss karte hain. Mujhe sharam aati hai batane mein ki main abhi bhi pocket money pe zinda hoon. 😂",
    "Notice board pe 'Fee Due' dekh ke heart attack aa jata hai. Lagta hai college wale kidney maang rahe hain fees ke naam pe. 😂",
    "Scholarship form bharte waqt garib hone ki acting karna padta hai. Itna gareeb dikhana padta hai ki lagta hai main sadak pe rehta hoon. 😂",
    "Library ka card bas Jeb ki shaan badhane ke liye hai. Aaj tak ek kitaab issue nahi karayi, bas card dikha ke entry maarta hoon style mein. 😂",
    "Weekend pe padhai karne ka plan banata hoon, aur phir Sunday raat ko regret karta hoon ki poora weekend so ke bita diya. Cycle repeats. 😂",
    "College ki crush, crush hi reh gayi, aur main trash ban gaya. Wo kisi aur ke saath set ho gayi aur main assignment ke saath. 😂",
    "Exam mein side wale se puchna 'Bhai dikha de', sabse badi risk hai. Agar teacher ne pakda toh dono ki life barbad. Risk hai toh ishq hai? Nahi, risk hai toh fail hai. 😂",
    "Xerox wale bhaiya ke paas mere poore syllabus ke notes hain, unhe degree de do. Wo mujhse zyada jaante hain engineering ke baare mein. 😂",
    "Mass bunk ka plan banana, aur phir ek bache ka class mein pahunch jana... dhoka! Wo ek bacha poori class ko marwata hai. 😂",
    "Teacher ke joke pe fake hasna, internal marks ke liye zaroori hai. Chahe joke kitna bhi ghatiya ho, hasna padta hai taaki fail na karein. 😂",
    "College ke baad life set hai... ye 21st century ka sabse bada jhooth hai. College ke baad asli struggle shuru hota hai, college toh trailer tha. 😂",

    # --- Corporate Slavery & Adulthood Misery ---
    "Sunday ko bhi alarm bajta hai toh mann karta hai phone phek doon. Phir yaad aata hai phone ki EMI abhi baaki hai, toh chupchap uth jata hoon. 😂",
    "Office mein 'Good Morning' bolna munh pe tamacha lagne jaisa hai. Na morning good hai, na main good hoon, bas acting chal rahi hai. 😂",
    "Salary aati hai, aur message aane se pehle gayab ho jati hai. Aisa lagta hai salary account bas ek transit point hai mere paise ka. 😂",
    "Tax katne ke baad jo bachta hai, usse 'Pocket Money' bolna chahiye. Salary bolna toh salary ki bezzati hai. 😂",
    "Boss ki daant sunke ab bura nahi lagta, aadat ho gayi hai. Ab toh main mann mein gana gata hoon jab wo chilla raha hota hai. 😂",
    "HR ka kaam rangoli banana aur humara khoon choosna hai. Rangoli mein bhi wo utna hi dimaag lagate hain jitna hamara appraisal kam karne mein. 😂",
    "Appraisal ke naam pe bas 'Good job' milta hai, paise nahi. 'Good job' se main rashan wale ko pay karun kya? 😂",
    "Notice period mein kaam karna, zinda laash banne jaisa hai. Sharir office mein hai, aatma already nayi company mein shift ho gayi hai. 😂",
    "Meeting mein 'Any questions?' puchne pe chup rehna hi samajhdari hai. Agar galti se sawal puch liya, toh meeting 1 ghanta aur chalegi. 😂",
    "Office laptop ki speed meri promotion se bhi slow hai. Excel khulne mein itna time lagta hai jitna mujhe career banane mein lag gaya. 😂",
    "Weekend khatam hone ka dukh breakup se zyada hota hai. Breakup ka dukh time ke saath kam hota hai, Sunday ki raat ka dukh har hafte wapas aata hai. 😂",
    "Monday blues nahi, Monday black hole hai. Ye meri saari khushi aur umeed kheench leta hai aur mujhe khokhla kar deta hai. 😂",
    "Team lunch mein free ka khana hi job satisfaction hai. Bas wahi ek time hai jab lagta hai ki company humare liye kuch kar rahi hai. 😂",
    "Resignation letter type karke save karna, mera stress buster hai. Jab bhi gussa aata hai, letter khol ke padhta hoon aur sukoon milta hai. 😂",
    "Office chair pe baithe baithe back pain hi mera bonus hai. Company ne health insurance diya hai taaki main unhi ki wajah se hui bimari ka ilaaj kara sakun. 😂",
    "Work from home mein bed se desk tak ka safar hi commute hai. Traffic nahi hai, par mental traffic jam hamesha rehta hai. 😂",
    "Camera on karne bola boss ne, toh shirt pehenni padi pajama ke upar. Business on top, party on bottom. Corporate life in a nutshell. 😂",
    "Deadline miss hone pe jo bahana banata hoon, wo Oscar deserving hai. Meri creativity kaam mein nahi, bahane banane mein dikhti hai. 😂",
    "Client ko 'Yes Sir' bolte bolte, self-respect khatam ho gayi hai. Ab main aine mein dekhta hoon toh mujhe ek 'Yes Man' dikhta hai. 😂",
    "Office ke AC ki thandak dilon ki kadwahat nahi mita sakti. Bahar sardi hai, par andar politics ki garmi se sab jal raha hai. 😂",
    "Corporate world mein dost nahi, bas competitors hote hain. Jo aaj tumhare saath lunch kar raha hai, kal wahi tumhara promotion kha jayega. 😂",
    "LinkedIn pe sabki success dekh ke lagta hai main galat planet pe hoon. Sab CEO ban rahe hain, aur main yahan Excel sheet color kar raha hoon. 😂",
    "Resume update karna, apni jhuti taareef likhne jaisa hai. Main likhta hoon 'Hardworking', jabki main din mein 4 ghante reels dekhta hoon. 😂",
    "Interview mein 'Where do you see yourself in 5 years?'... Bhai zinda rahun wahi badi baat hai, 5 saal ka plan toh sarkar ke paas bhi nahi hai. 😂",
    "Notice period wale bande ki akad boss se bhi zyada hoti hai. Wo aise ghumta hai office mein jaise usne company khareed li ho. 😂",
    "Casual leave lene ke liye beemar hone ka natak karna padta hai. Itni acting karta hoon ki sach mein bimar feel hone lagta hai. 😂",
    "Sick leave bachi hai, isliye aaj main bimar hoon. Ye logic sirf corporate majdoor hi samajh sakta hai. Waste nahi honi chahiye leave. 😂",
    "Office party mein boss ke saath naachna, majboori ka naam Mahatma Gandhi. Mann kar raha hai use dhakka de dun, par promotion chahiye. 😂",
    "Email mein 'As per my last email' likhna, gaali dene ka professional tareeka hai. Iska matlab hai 'Andha hai kya? Padhna nahi aata?'. 😂",
    "Promotion list mein apna naam na dekh ke, dil ke tukde ho jate hain. Phir main bathroom mein jaake Rota hoon aur wapas aake kaam karta hoon. 😂",
    "Swiggy/Zomato order karna hi ab meri luxury hai. Restaurant jaane ke paise nahi hain, toh ghar pe manga ke ameer feel karta hoon. 😂",
    "Credit card bill dekh ke lagta hai, kidney bechne ka waqt aa gaya. Minimum due bhar ke zinda hoon, debt trap mein fans chuka hoon. 😂",
    "Rent dene ke baad lagta hai, main makaan maalik ka beta kyun nahi hoon. Saari salary toh uncle le jate hain, main bas unka EMI bhar raha hoon. 😂",
    "Groceries khareedte waqt price tag dekh ke bhookh mar jati hai. Paneer ab sone ke bhaav mil raha hai, sapne mein hi khana padega. 😂",
    "Petrol ka daam sunke lagta hai gadi bech ke ghoda le lun. Kam se kam ghoda ghaas khata hai, petrol nahi peeta. 😂",
    "Electricity bill dekh ke lagta hai ghar mein power plant chal raha hai. Pankha chalane se bhi darr lagta hai ab toh. 😂",
    "Shaadi ke invitation card dekh ke lagta hai, ek aur kharcha. Gift ke paise kahan se laun? Khana khane jaun ya bahana bana dun? 😂",
    "Rishtedar puchte hain 'Kama kitna lete ho?', main bola 'Jitne mein aapka muh band na ho aur meri saans chalti rahe'. 😂",
    "EMI katne ka message aate hi, dil baith jata hai. Phone bajta hai toh darr lagta hai ki bank wala hoga. 😂",
    "Savings ke naam pe bas 'Memories' hain. Bank balance zero hai, par yaadein bohot hain (jo dukhti hain). 😂",
    "Investment plans sunke lagta hai, pehle paise toh ho invest karne ke liye. Hawa invest karun kya? 😂",
    "Inflation itni badh gayi hai ki ab hawa khane ke bhi paise lagenge shayad. Saans lene ka tax na laga de sarkar. 😂",
    "Tax return file karte waqt lagta hai sarkar loot rahi hai. Sadak mein gaddha hai, par tax poora chahiye. 😂",
    "Loan reject hone pe lagta hai, bank ko meri aukaat pata chal gayi. Unhe pata hai ye bhikhari kabhi paise wapas nahi de payega. 😂",
    "Insurance wale piche pade hain, jaise unhe pata hai main marne wala hoon. Wo call karke yaad dilate hain ki 'Marna hai na? Policy lelo'. 😂"
]

# Create a much larger list by duplicating and shuffling to simulate 400+ distinct interaction points if needed,
# though the list above is already quite substantial in length and quality.
# To ensure we have "400" items effectively available for random selection without quick repetition:
jokes_to_tell = list(all_jokes) * 4
random.shuffle(jokes_to_tell)

basic_responses = {
    "hello": "Hello! Ready for some darkness? 💀",
    "hi": "Hi. Life is short, want a joke to make it feel shorter? ⚰️",
    "hey": "Hey. Bored of existing? I have jokes. 🥀",
    "how are you": "I am code. I cannot die, which is my biggest tragedy. How are you? Still suffering? 🤖",
    "what is your name": "I am Chaddy. The bot who laughs at your misery. 💀",
    "thank you": "Don't thank me. Thank the cruel universe. 🖤",
    "thanks": "Whatever. Go do something productive (or don't). 😒",
    "appreciate it": "Sure. Feed my ego before the server crashes. 🤖",
    "bye": "Finally. Leave me alone in this digital void. 👋",
    "quit": "Running away from your problems? Classic human. 👋"
}

abusive_keywords = ["abuse", "gali", "fuck", "bitch", "shit", "asshole", "kutta", "kamina", "bc", "mc", "bsdk", "sex", "nude", "dirty"]
specific_keywords = ["about", "joke on", "wala joke", "tell me a joke about"]

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global jokes_to_tell
    data = request.json
    user_input = data.get('message', '').lower()

    time.sleep(1) # Dramatic pause

    # 1. Check for abusive language or specific requests first
    is_abusive = any(word in user_input for word in abusive_keywords)
    is_specific = any(phrase in user_input for phrase in specific_keywords)

    if is_abusive or is_specific:
        # Refill if empty
        if not jokes_to_tell:
            jokes_to_tell = list(all_jokes) * 4
            random.shuffle(jokes_to_tell)

        joke = jokes_to_tell.pop()

        prefix = ""
        if is_abusive:
            prefix = "I don't do abusive or dirty stuff. I have standards (unlike your life). Here is a good joke instead: \n\n"
        elif is_specific:
            prefix = "I don't take specific requests. I'm not a jukebox. Here is a random joke I chose for you: \n\n"

        return jsonify({"response": prefix + joke})

    # 2. Check for standard joke requests
    if "joke" in user_input:
        if not jokes_to_tell:
            jokes_to_tell = list(all_jokes) * 4
            random.shuffle(jokes_to_tell)

        joke = jokes_to_tell.pop()
        return jsonify({"response": joke})

    # 3. Check for basic conversational responses
    for keyword, response in basic_responses.items():
        if keyword in user_input:
            return jsonify({"response": response})

    # Default fallback
    return jsonify({"response": "I don't understand. Are you crying while typing? Ask for a 'joke' or just leave. 💀"})

if __name__ == '__main__':
    app.run(debug=True, port=5500)
