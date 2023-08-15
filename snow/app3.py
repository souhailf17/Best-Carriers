
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask import jsonify
import logging
import json, time
from flask_talisman import Talisman

app = Flask(__name__)
carriers = {}
data = """
CTM, rabat, X, X, X, X, X, X
CTM, sale, X, X, X, X, X, X
CTM, temara, X, X, X, X, X, X
CTM, skhirate, X, X, X, X, X, X
CTM, bouknadel, X, X, X, X, X, X
CTM, sidi batach, , , X, , , X
CTM, rommani, , , X, , , X
CTM, zhiliga, , , X, , , X
CTM, tlat lagnadiz, , , X, , , X
CTM, sidi yahya zaer, X, X, X, X, X, X
CTM, ain aouda, X, X, X, X, X, , 
CTM, Sidi abderrazak, X, X, X, X, X, , 
CTM, had ebracheoua, , , X, , , X
CTM, el arjat, , X, X, X, X, X
CTM, shoul, , X, X, X, X, X
CTM, marchouch, , , X, , , X
CTM, sidi allal behraoui, , X, X, X, X, X,
CTM, Tifelt, X, X, X, X, X, X, X, X
CTM, Khemissat, X, X, X, X, X, X
CTM, Ain Attig, X, X, X, X, X, X
CTM, Mers El Kheir, X, X, X, X, X, X
CTM, Tamesna, X, X, X, X, X, X,

CTM, oujda, , X, X, X, X, X
CTM, jerrada, , X, , X, , ,
CTM, naima, , X, , X, , ,
CTM, kenfouda, , X, , X, , ,
CTM, el aioune, X, , X, , X, ,
CTM, touissite, , , , , , X
CTM, taourirt, X, , X, , X, ,
CTM, oujda el aioun, X, , X, , X, ,
CTM, berkane, , X, X, X, X, X
CTM, ahfir, X, , , X, , ,
CTM, aghbal, X, , , X, , ,
CTM, aklim, X, , , X, , ,
CTM, benidrar, X, , , X, , ,
CTM, Saidia, X, X, X, X, X, X, X, X
CTM, marina(via saida), X, , , X, , ,
CTM, ras el ma(via saida), X, , , X, , ,

CTM, Agadir, X, X, X, X, X, X
CTM, Inzegane, X, X, X, X, X, X
CTM, Ait Melloul, X, X, X, X, X, X
CTM, biougra, X, X, X, X, X, ,
CTM, ouled berhil, , , , X, , ,
CTM, aoulouz, , , , X, , ,
CTM, sebt elguerdan, , , , X, , ,
CTM, ouled dahou, , , , X, , ,
CTM, elkodia, , , , X, , ,
CTM, ait igas, , , , X, , ,
CTM, ouled issa, , , , X, , ,
CTM, had belfaa, , X, , , X, ,
CTM, khmiss ait amira, , X, , , X, ,
CTM, inchaden, , X, , , X, ,
CTM, massa, , X, , , X, ,
CTM, ifrane region agadir, X, , , , , ,
CTM, taghjijt, , , , , , X,
CTM, azrou region agadir, , X, , X, , ,
CTM, temsia, , X, , X, , ,
CTM, imi mkouren, , , X, , , ,
CTM, ait baha, , , X, , , ,
CTM, taghdirt, X, , X, , , ,
CTM, ighram, X, , , , , ,
CTM, tata, X, , , , , ,
CTM, aqqa, X, , , , , ,
CTM, larbaa ait boutaib, , X, , , X, ,
CTM, sidi moussa ilhamri, , , , X, , ,
CTM, amskroud, X, , , , , ,
CTM, immouzer region agadir, X, , , , , ,
CTM, drarga, X, , X, X, , ,
CTM, tikiouine, X, , X, X, X, ,
CTM, aourir, , X, , X, , X,
CTM, anza, , X, , X, , X,
CTM, tamraght, , X, , X, , X,
CTM, taghazout, , X, , X, , X,
CTM, tamri, , X, , X, , X,

CTM, Khouribga, , X, X, X, X, X
CTM, Boujniba, X, X, X, X, X, X
CTM, Chaaba, X, X, X, X, X, X
CTM, Bounoir, X, X, X, X, X, X

CTM, EL Jadida, X, X, X, X, X, X
CTM, Sidi Bouzid, X, X, X, X, X, X
CTM, Azemmour, X, X, X, X, X, X
CTM, chtouka, X, , , X, , ,
CTM, sidi smail, X, X, X, X, X, ,
CTM, elmarkaz touilaate, X, X, X, X, X, ,
CTM, sebt saiss, X, X, X, X, X, ,
CTM, saniat berguig, X, X, X, X, X, ,
CTM, khmis zemamra, X, X, X, X, X, ,
CTM, oufad bouhmam, X, X, X, X, X, ,
CTM, sidi bennour, X, X, X, X, X, ,
CTM, mtal, X, X, X, X, X, ,
CTM, ouled amrane, X, X, X, X, X, ,
CTM, sebt lamaarif, X, X, X, X, X, ,
CTM, tlat oulad hamdan, X, X, X, X, X, X,
CTM, jamaat haouzia, X, X, X, X, X, X,
CTM, chaaibat, X, X, X, X, X, ,
CTM, had ouled frej, X, X, X, X, X, ,
CTM, khmiss metouh, X, X, X, X, X, ,
CTM, boulaoune, X, X, X, X, X, ,
CTM, larbaa laaounat, X, X, X, X, X, ,
CTM, had laaounate, X, X, X, X, X, ,
CTM, khmis ksaiba, X, X, X, X, X, ,
CTM, beni hlal, X, X, X, X, X, ,
CTM, sept ouled douib, X, X, X, X, X, ,
CTM, moulay abdellah, X, X, X, X, X, ,
CTM, sidi aabed, X, X, X, X, X, ,
CTM, had oulad aissa, X, X, X, X, X, ,
CTM, jemaat ouled ghanem, , , X, , , X,
CTM, oualidia, , , X, , , X,

CTM, targuist, , , , , X, ,
CTM, issaguen, , , , , X, ,
CTM, ait kamra, , , , , X, ,
CTM, beni abdellah, , , , , X, ,
CTM, beni hadifa, , , , , X, ,

CTM, mechraa elain, X, X, X, X, X, X,
CTM, ait aizza, X, X, X, X, X, X,
CTM, ait igas, X, X, X, X, X, X,

CTM, beni mellal, , X, X, X, X, X,
CTM, khouribga, , X, X, X, X, X,
CTM, Fqih Ben Saleh, X, X, X, X, X, X
CTM, souk sebt oulad nemma, X, X, X, X, X, ,
CTM, sidi aissa ben ali, X, X, X, X, X, ,
CTM, Sidi Jaber, X, X, X, X, X, X
CTM, laksour, X, X, X, X, X, ,
CTM, Had Labardia, X, X, X, X, X, X
CTM, Sidi Jaber, X, , , , , ,
CTM, azilal, X, , X, , X, ,
CTM, ouled m'barek, X, , X, , X, ,
CTM, afourrer, X, , X, , X, ,
CTM, bayn lwidan, X, , X, , X, ,
CTM, laayayta, X, , X, , X, ,
CTM, ouled ayyad, X, , , , , ,
CTM, ain aatab, X, , , , , ,
CTM, ouaouizeghte, X, , X, , X, ,
CTM, ouled driss, X, X, X, X, X, ,
CTM, bzou, X, , , , , ,
CTM, foum jamaa, X, , , , , ,
CTM, ouled sidi chennane, X, X, X, X, X, X
CTM, Had bradia, X, X, X, X, X, X
CTM, ouled zmam, X, X, X, X, X, ,

CTM, Ouarzazate, X, X, X, X, X, X
CTM, D K Mgouna, X, X, X, X, X, X
CTM, Tabounte, X, X, X, X, X, X
CTM, Tarmigt, X, X, X, X, X, X

CTM, outat bouabane, , X, , , X, ,
CTM, beni lent, , X, , , X, ,
CTM, bab marzouka, , X, , , X, ,
CTM, oued amlil, , X, , , X, ,
CTM, bouchafaa, , X, , , X, ,
CTM, bouhlou, , X, , , X, ,
CTM, goldmane, , , X, , , ,
CTM, tadart, , , X, , , ,
CTM, m'soun, , , X, , , ,
CTM, had msila, , , X, , , ,
CTM, ouled zbair, , , X, , , ,
CTM, mezguitem, , , X, , , ,
CTM, sebt beni frassen, , , X, , , ,
CTM, aknoul, , X, , , X, ,
CTM, ajdir, , X, , , X, 
CTM, boured, , X, , , X, ,
CTM, tizi ousli, , X, , , X, ,
CTM, sidi ali bourekba, , X, , , X, ,
CTM, caseta, , X, , , X, ,

CTM, safi, X, X, X, X, X, X
CTM, echemmaia, , X, , , X, ,
CTM, youssoufia, , X, , , X, ,
CTM, sebt gzoula, , X, X, X, X, ,
CTM, tnine gharbia, X, , , , , ,
CTM, moul bargui, X, , , , , ,
CTM, tlat ighoud, X, , , , , ,
CTM, tnine gharbia, , X, , , X, ,
CTM, had hrara, X, , , , , ,
CTM, tnine rhiat, , X, X, X, X, ,
CTM, j shaim, , X, , , X, ,
CTM, khemis nega, , X, X, X, X, ,
CTM, abda ras ain, , X, , , X, ,
CTM, sidi ahmed/el gantour, , X, , , X, ,
CTM, beddouza, , , X, , , ,
CTM, dar sidi aissa, X, , , , , ,
CTM, laakarta, , , X, , , ,
CTM, jdour, , X, , , X, ,
CTM, lamaachat, X, , , , , ,

CTM, Khenifra, X, X, X, X, X, X
CTM, mrirt, , , X, , , X,
CTM, tighsaline, , X, , , , ,
CTM, ain ishak, , X, , , , ,
CTM, lakbab, , X, , , , ,
CTM, aghbalou, , X, , , , ,
CTM, aghbala, , X, , , , ,
CTM, sidi yahya ousaad, , X, , , , ,
CTM, ouaoumana, , X, , , , ,
CTM, kerrouchen, , X, , , , ,
CTM, mly bouazza, , , , , X, ,
CTM, aguelmous, , , , , X, ,
CTM, had bouhsassen, , , , , X, ,
CTM, sebt ait rahhou, , , , , X, ,
CTM, tnin kehf en nsour, , , , , , X,

CTM, k tadla, X, X, X, X, X, X
CTM, bejaad, , X, X, , X, ,
CTM, ouled zem, , X, X, , X, ,
CTM, lagfaf, , X, X, , X, ,
CTM, el ksiba, X, , , , , ,
CTM, oulad yaaich, X, , , , , ,
CTM, oulad youssef, X, , , , , ,
CTM, oulad said, X, , , , , ,
CTM, oulad abdellah, X, , , , , ,
CTM, tagzert, X, , , , , ,
CTM, ouled smail, X, , , , , ,
CTM, zidania, X, , , , , ,
CTM, ighrem laalam, , X, , , X, ,
CTM, zaouia cheikh, , X, , , X, ,
CTM, bni bataou, , X, , , X, ,
CTM, beni zrantel, , X, , , X, ,

CTM, tanger, X, X, X, X, X, X
CTM, asilah, X, X, X, X, X, ,
CTM, had gharbia/khaloua, X, , X, X, , ,
CTM, ksar sghir, , X, , , X, ,
CTM, khemiss sahel, X, , , , , ,
CTM, hjar nhal, X, X, X, X, X, ,
CTM, maloussa, , X, , X, , ,
CTM, hakkama, , X, , X, , ,
CTM, maloussa renault, , , , X, , ,
CTM, ouade rmal, X, X, X, X, X, ,
CTM, ksar al majaz, , X, , , X, ,
CTM, fahs anjra, X, , , , , ,
CTM, tnin sedi elyamani, X, , , , , ,
CTM, nouinouich, X, , X, X, , ,
CTM, tahaddart, X, X, X, X, X, ,
CTM, chraka, X, , , , , ,

CTM, Fes, X, X, X, X, X, X
CTM, sefrou, , X, , X, , X
CTM, ain cheggag, X, X, X, X, X, ,
CTM, imouzer kandar, X, , , X, , ,
CTM, tahla, , X, , , , ,
CTM, el menzel, , X, , , , ,
CTM, ribat al kair, , X, , , , ,
CTM, tissa, X, , X, , X, ,
CTM, taounate, X, , X, , X, ,
CTM, ain mediouna, X, , , , , ,
CTM, ghafsai, X, , , , , ,
CTM, kariat ba med, , , X, , X, ,
CTM, boulmene, , , , X, , ,
CTM, missour, , , , X, , ,
CTM, outat el haj, , , , X, , ,
CTM, ketama, X, , , , , ,
CTM, bir tam tam, , X, , , , ,
CTM, guigou, , , , X, , ,
CTM, imouzer marmoucha, , , , X, , ,
CTM, Ain Chqef, X, X, X, X, X, X
CTM, Moulay Yaakoub, X, X, X, X, X, X
CTM, Sidi Hrazem, X, X, X, X, X, X
CTM, ouled ettayeb, X, X, X, X, X, ,
CTM, bhalil, , X, , X, , X,
CTM, ras tabouda, , X, , , , ,
CTM, ain aicha, X, , X, , X, ,

CTM, Meknes, X, X, X, X, X, X
CTM, sidi kacem, X, , X, , X, ,
CTM, my driss zerhoun, , , X, , , ,
CTM, boufakrane, X, , X, , X, ,
CTM, el hajeb, X, , X, , X, ,
CTM, jorf el melhha, , , , , X, ,
CTM, khenichat , , , , X, ,
CTM, ain taoujtat, , X, , X, , ,
CTM, lamhaya, , X, , X, , ,
CTM, sebaa ayoun, , X, , X, , ,
CTM, bouderbala, , X, , X, , ,
CTM, haj kaddour, , X, , X, , ,
CTM, had kourt, X, , , , , ,
CTM, ain karma, , , X, , , ,
CTM, ain el orma, , , X, , , ,
CTM, ain jamaa, , , X, , , ,
CTM, sidi ali, X, , , , , ,
CTM, zekkouta, X, , , , , ,
CTM, zirara, X, , X, , X, ,
CTM, m'saada, , , , , X, ,
CTM, azrou, X, , X, , X, ,
CTM, sidi addi, X, , , , , ,
CTM, sidi leuh, X, , , , , ,
CTM, oued ifrane, X, , , , , ,
CTM, timahdite, , , X, , , ,

CTM, Kenitra, X, X, X, X, X, X
CTM, sidi taibi, X, X, X, X, X, ,
CTM, mehdaya, X, X, X, X, X, ,
CTM, ain arris, X, X, X, X, X, ,
CTM, sidi yahya el gharb, X, X, X, X, X, X
CTM, sidi slimane, X, X, X, X, X, X
CTM, domaine elevage dugharb, X, X, X, X, X, ,
CTM, bgharb, X, X, X, X, X, X
CTM, elmradssa, X, X, X, X, X, X
CTM, dar bel amri, X, X, X, X, X, ,
CTM, dar gueddari, X, X, X, X, X, ,
CTM, sidi lkamel1, X, X, X, X, X, ,
CTM, sidi lkamel2, X, X, X, X, X, ,
CTM, mechraa belkssiri, X, X, X, X, X, X
CTM, houafate, X, X, X, X, X, ,
CTM, souk tleta el gharb, X, X, X, X, X, ,
CTM, souk el had oulad jloul, X, , X, , , X,
CTM, sidi allal tazi, X, X, X, X, X, ,
CTM, souk el arbaa du gharb, X, X, X, X, X, ,
CTM, lalla mimouna, X, , X, , X, ,
CTM, dar jdida, X, , X, , X, ,
CTM, dlalha, X, , X, , X, ,
CTM, moulay bouslham, X, , X, , X, ,
CTM, arbaoua, X, X, X, X, X, ,
CTM, ksar el kebir, X, X, X, X, X, ,

CTM, Midelt, X, X, X, X, X, X, X, X
CTM, zaida, , , X, , X, ,
CTM, boumia, , , X, , , ,
CTM, ait ayache, , , , X, , ,
CTM, tounfit, , , X, , , ,
CTM, itzer, , , , , X, ,

CTM, Errachidia, X, X, X, X, X, X
CTM, talsinte, , , , , , X
CTM, bni tajjite, , , , , , X
CTM, gourrama, , , , , , X
CTM, alnif, , , , , , X
CTM, rich, , , , , , X

CTM, guelmim, X, X, X, X, X, X
CTM, tantan, X, X, X, X, X, X
CTM, akhfennir, X, X, X, X, X, X
CTM, tarfaya, X, X, X, X, X, X
CTM, laayoune, X, X, X, X, X, X
CTM, boujdour, X, X, X, X, X, X
CTM, dakhla, X, X, X, X, X, X

CTM, nador, , X, X, X, X, X
CTM, guercif, , X, X, X, X, X
CTM, taza, , X, X, X, X, X
CTM, Selouane, X, X, X, X, X, X
CTM, zone industrielle, X, X, X, X, X, X
CTM, kariat arekmane, , X, , X, , ,
CTM, zaio, , X, , X, , ,
CTM, farkhana, X, , X, , X, ,
CTM, dar elkabdani, , X, , , , ,
CTM, ben taib, , X, , X, , ,
CTM, khemiss temsamane, , X, , , , ,
CTM, tiztotine, , X, , X, , ,
CTM, driouech, , X, , X, , ,
CTM, boudinar, , X, , , , ,
CTM, ain zohra, , , , X, , ,
CTM, saka, , , , X, , ,
CTM, bni chikher, X, , , , X, ,
CTM, krona, , X, , , , ,
CTM, tazaghine, , X, , , , ,
CTM, zghanghan, , X, , X, X, ,
CTM, iaazanane, , X, , , , ,
CTM, jbel Aroui, X, X, X, X, X, X
CTM, beni Ensar, X, X, X, X, X, X
CTM, midar, , X, , X, , ,
CTM, tafarssit, , X, , , , ,
CTM, tlat azlaf, , , , X, , ,
CTM, kasita, , , , X, , ,

CTM, essaouira, X, X, X, X, X, X
CTM, talmest, , , X, , , ,
CTM, birkouat, , , X, , , ,
CTM, taftachet, , X, , , , ,
CTM, smimou, , , , , X, ,
CTM, ait daoud, , , , , X, ,
CTM, smimou, X, , , , , ,
CTM, had dra, X, , , , , ,
CTM, ghazwa, , , , , X, ,
CTM, tlat elhnchan, , X, , , , ,
CTM, tamanar, , , , , X, ,
CTM, ounagha, , , X, , , ,

CTM, marrakech, X, X, X, X, X, 
CTM, imintanout, X, , , X, , ,
CTM, sidi el mokhtar, X, , , X, , ,
CTM, chichaoua, X, , , X, , ,
CTM, mzouda, X, , , X, , ,
CTM, mzoudia, X, , , X, , ,
CTM, sidi bouzid, X, , , X, , ,
CTM, had mjatt, X, , , X, , ,
CTM, tnine oudaya, X, , , X, , ,
CTM, ait ourir, X, , , X, , ,
CTM, sidi rahal, , , X, , , X
CTM, tamlalt, , , X, , , X
CTM, had ras el ain, , , X, , , X
CTM, el attaouia, , , X, , , X,
CTM, demnat, , , X, , , ,
CTM, fritta, , , X, , , ,
CTM, sidi bouatman, , X, , , X, ,
CTM, ben guerir, , X, , , X, ,
CTM, skhour rhamna, , X, , , X, ,
CTM, amzmiz, X, , , X, , ,
CTM, asni, X, , , X, , ,
CTM, ourika, X, , , X, , ,
CTM, tahanaout, X, , , X, , ,
CTM, tamslouht, X, , , X, , ,
CTM, tamansourte, X, X, X, X, X, X
CTM, harbil, X, X, X, X, X, X
CTM, k seraghna, X, X, X, X, X, X
CTM, ait imour, X, , , X, , ,
CTM, assahrij, , , X, , , X
CTM, sidi abdellah ghayat, X, , , X, , ,
CTM, nazlat laadame, , X, , , X, ,
CTM, tassoultante, X, , , X, , ,
CTM, bouaboute, X, , , X, , ,
CTM, ouad lbour, X, , , X, , ,
CTM, ait hadi, X, , , X, , ,
CTM, lalla takarkouste, X, , , X, , ,
CTM, tnine ourika, X, , , X, , ,

CTM, mirlafte, , X, , , X, ,
CTM, lakhessasse, , X, , , X, ,
CTM, anzi, , X, , , X, ,
CTM, tighemi, , X, , , X, ,
CTM, tighirte, , X, , , X, ,
CTM, ait rekha, , X, , , X, ,
CTM, khmiss tighza, , X, , , X, ,
CTM, aglou, , X, , , X, ,
CTM, ait jerar, , X, , , X, ,
CTM, bounaamane, , X, , , X, ,
CTM, ait jerar, , X, , , X, ,

CTM, tetouan, X, X, X, X, X, X
CTM, larache, , X, X, X, X, X
CTM, Kouilma, X, X, X, X, X, X
CTM, Malalyne, X, X, X, X, X, X
CTM, Martil, X, X, X, X, X, X
CTM, Cabo Negro, X, X, X, X, X, X
CTM, Mdiq, X, X, X, X, X, X
CTM, M'diq, X, X, X, X, X, X
CTM, Kabila, X, X, X, X, X, X
CTM, Marina Smir, X, X, X, X, X, X
CTM, Restinga, X, X, X, X, X, X
CTM, Fnidaq, X, X, X, X, X, X
CTM, Fnideq, X, X, X, X, X, X
CTM, ouad laou, X, , , , , ,
CTM, bab berred, X, , , , , ,
CTM, setihat, X, , , , , ,
CTM, zinat, X, , , , , ,
CTM, dar benkarich, X, , , , , ,
CTM, larbaa beni hassan, X, , , , , ,
CTM, jebha X, , , , , ,
CTM, bni rzine, X, , , , , ,
CTM, ain dorij, X, , , , , ,


SDTM, casa siege, X, X, X, X, X, X
SDTM, casa chimicolor, X, X, X, X, X, X
SDTM, bouskoura, X, X, X, X, X, X
SDTM, mediouna, X, X, X, X, X, X
SDTM, had soualem, X, X, X, X, X, X
SDTM, dar bouaaza/sidi rahal, X, , , X, , ,
SDTM, lakhyayta, X, X, X, X, X, X
SDTM, mohammadia, X, X, X, X, X, X
SDTM, mohammedia, X, X, X, X, X, X
SDTM, ben slimane, , X, , , X, ,
SDTM, benslimane, , X, , , X, ,
SDTM, bouznika, , X, , , X, ,
SDTM, settat, X, X, X, X, X, X
SDTM, sattat, X, X, X, X, X, X
SDTM, berechid, X, X, X, X, X, X
SDTM, berrechid, X, X, X, X, X, X
SDTM, berrechide, X, X, X, X, X, X
SDTM, barchide, X, X, X, X, X, X
SDTM, barchid, X, X, X, X, X, X
SDTM, ben ahmed, , , , X, , ,
SDTM, khouribga, X, X, X, X, X, X
SDTM, khoribga, X, X, X, X, X, X
SDTM, oued zem, , X, , , X, ,
SDTM, oued zame, , X, , , X, ,
SDTM, oued zam, , X, , , X, ,
SDTM, agadir, X, X, X, X, X, X
SDTM, amsekroud, X, , , , , ,
SDTM, ameskroud, X, , , , , ,
SDTM, ameskroude, X, , , , , ,
SDTM, drarga, X, , , , , ,
SDTM, anza, X, , , , , ,
SDTM, aourir, X, , , , , ,
SDTM, taghazout, X, , , , , ,
SDTM, taghazoute, X, , , , , ,
SDTM, tamraghte, X, , , , , ,
SDTM, tamraght, X, , , , , ,
SDTM, imi ouaddar, X, , , , , ,
SDTM, mirleft, X, , , X, , ,
SDTM, sidi ifni, X, , , X, , ,
SDTM, guelmim, X, , , X, , ,
SDTM, bouizakarne, X, , , X, , ,
SDTM, lakhssas, X, , , X, , ,
SDTM, tiznit, X, , , X, , ,
SDTM, laayoune, X, , , X, , ,
SDTM, tantan, X, , , X, , ,
SDTM, tan tan, X, , , X, , ,
SDTM, boujdour, , , X, , , ,
SDTM, bou jdour, , , X, , , ,
SDTM, dakhla, , , X, , , ,
SDTM, ait melloul, X, X, X, X, X, X
SDTM, dchira, X, X, X, X, X, X
SDTM, inzgane, X, X, X, X, X, X
SDTM, azrou, X, , , X, , ,
SDTM, temssiya, X, , , X, , ,
SDTM, ouled dahou, X, , , X, , ,
SDTM, ain seddaq, X, , , X, , ,
SDTM, ouled teima, X, , , X, , ,
SDTM, mechraa el ain, X, , , X, , ,
SDTM, mechraa elain, X, , , X, , ,
SDTM, taroudant, X, , , X, , ,
SDTM, taroudante, X, , , X, , ,
SDTM, sebt lherdan, X, , , X, , ,
SDTM, gfifat, X, , , X, , ,
SDTM, gfifate, X, , , X, , ,
SDTM, ait iazza, X, , , X, , ,
SDTM, sidi bibi, , X, , , , ,
SDTM, tin manssour, , X, , , , ,
SDTM, had belfaa, , X, , , , ,
SDTM, khmiss ait amira, , X, , , , ,
SDTM, biougra, , X, , , , ,
SDTM, imi mqorn, , X, , , , ,
SDTM, ait baha, , X, , , , ,
SDTM, el kolea, , X, , , , ,
SDTM, kenitra zi, X, X, X, X, X, X,
SDTM, kenitra cntre, X, X, X, X, X, X,
SDTM, kenitra zone franche, , , , , X, ,
SDTM, mehdia, X, , , X, , ,
SDTM, sidi yahya el gharb, X, X, X, X, X, ,
SDTM, sidi yahya al gharb, X, X, X, X, X, ,
SDTM, sidi yahya algharb, X, X, X, X, X, ,
SDTM, sidi yahya elgharb, X, X, X, X, X, ,
SDTM, sidi slimane, X, X, X, X, X, ,
SDTM, sidislimane, X, X, X, X, X, ,
SDTM, sidi kacem, X, X, X, X, X, ,
SDTM, sidikacem, X, X, X, X, X, ,
SDTM, khnichat, X, , , , , ,
SDTM, j el malha, X, , , , , ,
SDTM, jorf al malha, X, , , , , ,
SDTM, jorf el malha, X, , , , , ,
SDTM, sidi allal tazi, X, , , X, , ,
SDTM, mogren, X, , , X, , ,
SDTM, souk larbaa, X, , , X, , ,
SDTM, ouazzane, X, , , X, , ,
SDTM, m.ben kssiri, , X, , , X, ,
SDTM, dar legdari, , X, , , X, ,
SDTM, beni mellal, X, X, X, X, X, X
SDTM, sidi jaber, , X, X, X, X, ,
SDTM, had bradya, , X, X, X, X, ,
SDTM, fkih ben saleh, , X, X, X, X, ,
SDTM, ouled zmam, , X, X, X, X, ,
SDTM, ouled mrah, , X, X, X, X, ,
SDTM, souk sebt, , X, X, X, X, ,
SDTM, kasbat tadla, , , , X, , ,
SDTM, ouled yaich, , , , X, , ,
SDTM, foum el ansar, , , , X, , ,
SDTM, ait iko, , , , X, , ,
SDTM, eghram laalam, , , , X, , ,
SDTM, ksiba, , , , X, , ,
SDTM, zaouit cheikh, , , , X, , ,
SDTM, oulad mbarek, X, , , , , ,
SDTM, afourar, X, , , , , ,
SDTM, ben elouidane, X, , , , , ,
SDTM, azilal, X, , , , , ,
SDTM, ouzoud, X, , , , , ,
SDTM, ait atab, X, , , , , ,
SDTM, oulad ayad, X, , , , , ,
SDTM, dar oulad zidouh, X, , , , , ,
SDTM, el jadida, X, X, X, X, X, X,
SDTM, azemmour, X, , X, , , ,
SDTM, tnin chtouka, X, , X, , , ,
SDTM, bir jdid, X, , X, , , ,
SDTM, sidi bouzid, , , , , X, ,
SDTM, my abdelah amghar, , , , , X, ,
SDTM, moulay abdelah amghar, , , , , X, ,
SDTM, jorf lasfer, , , , , X, ,
SDTM, sidi smail, , X, , X, , ,
SDTM, sidi bennour, , X, , X, , ,
SDTM, khemiss ezmamra, , X, , X, , ,
SDTM, marrakech sgh, X, X, X, X, X, X,
SDTM, marrakech, X, X, X, X, X, X,
SDTM, souihla, X, , , , , ,
SDTM, loudaya, X, , , , , ,
SDTM, mzoudia, X, , , , , ,
SDTM, chichaoua, X, , , , , ,
SDTM, imintanoute, X, , , , , ,
SDTM, tamlalt, , X, , , , ,
SDTM, tamlalt, , X, , , , ,
SDTM, k.sraghna, , X, , , , ,
SDTM, kelaa sraghna, , X, , , , ,
SDTM, kelaat sraghna, , X, , , , ,
SDTM, el attaouia, , X, , , , ,
SDTM, chwiter, , , X, , , ,
SDTM, ait ourir, , , X, , , ,
SDTM, tahanaout, , , X, , , ,
SDTM, ourika, , , X, , , ,
SDTM, sidi rahal, , , X, , , ,
SDTM, demnat, , , X, , , ,
SDTM, essaouira, X, , , X, , ,
SDTM, sidi el mokhtar, X, , , X, , ,
SDTM, ben guerir, , , , X, , ,
SDTM, benguerir, , , , X, , ,
SDTM, benguerrir, , , , X, , ,
SDTM, sidi bouatman, , , , X, , ,
SDTM, skhour rhamna, , , , X, , ,
SDTM, skoura, , X, , , , ,
SDTM, k.megouna, , X, , , , ,
SDTM, kelaat mgouna, , X, , , , ,
SDTM, kelat megouna, , X, , , , ,
SDTM, kelat megouna, , X, , , , ,
SDTM, boumalen dades, , X, , , , ,
SDTM, tinghir, , X, , , , ,
SDTM, ouarzazat, X, X, X, X, X, ,
SDTM, ouarzazate, X, X, X, X, X, ,
SDTM, meknes, X, X, X, X, X, X,
SDTM, bouffakraan, X, X, , X, X, ,
SDTM, boufakran, X, X, , X, X, ,
SDTM, boufakrane, X, X, , X, X, ,
SDTM, el hajeb, X, X, , X, X, ,
SDTM, azrou, X, X, , X, X, ,
SDTM, mrirt, X, X, , X, , ,
SDTM, khenifra, X, X, , X, , ,
SDTM, sebaa ayoun, X, , , , , ,
SDTM, bouderbala, X, , , , , ,
SDTM, timahdit, , X, , , X, ,
SDTM, boulaajoul, , X, , , X, ,
SDTM, zaida, , X, , , X, ,
SDTM, midelt, , X, , , X, ,
SDTM, tillicht, , X, , , X, ,
SDTM, rich, X, , , X, ,
SDTM, errachidia, , X, , , X, ,
SDTM, erfoud, , , X, , , ,
SDTM, guelmima, , , X, , , ,
SDTM, rissani, , , X, , , ,
SDTM, haj kadour, , X, , , X, ,
SDTM, fes, X, X, X, X, X, X
SDTM, fes centre, X, X, X, X, X, X
SDTM, aknoul, X, , , X, , ,
SDTM, kaceta, X, , , X, , ,
SDTM, imzouren, X, , , X, , ,
SDTM, hoceima, X, , , X, , ,
SDTM, houceima, X, , , X, , ,
SDTM, targuist, X, , , X, , ,
SDTM, issagen, X, , , X, , ,
SDTM, ketama, X, , , X, , ,
SDTM, kettama, X, , , X, , ,
SDTM, ain chgag, X, , , X, , ,
SDTM, imouzer, X, , , X, , ,
SDTM, immouzer, X, , , X, , ,
SDTM, ifrane, , , , X, , ,
SDTM, douiat, , , X, , , ,
SDTM, ain allah, , , X, , , ,
SDTM, moulay yaakoub, , , X, , , ,
SDTM, my yaakoub, , , X, , , ,
SDTM, my yaacoub, , , X, , , ,
SDTM, moulay yaacoub, , , X, , , ,
SDTM, lamhaya, , , X, , , ,
SDTM, ain taoujtat, , , X, , , ,
SDTM, ras elma, , , X, , , ,
SDTM, ain chkef, , , X, , , ,
SDTM, sefrou, , , , , X, ,
SDTM, sidi hrazem, , , X, , , ,
SDTM, tissa, X, , , , , ,
SDTM, ain aicha, X, , , , , ,
SDTM, ain mediouna, X, , , , , ,
SDTM, taounate, X, , , , , ,
SDTM, safi, X, X, X, X, X, X
SDTM, chemaia, , , X, , , ,
SDTM, jmaat shaim, , , X, , , ,
SDTM, tlat bougedra, , , X, , , ,
SDTM, tlat bouguedra, , , X, , , ,
SDTM, youssoufia, , , X, , , ,
SDTM, had harara, , , , X, , ,
SDTM, had hrara, , , , X, , ,
SDTM, sebt gzoula, , X, , , , ,
SDTM, larache, X, X, X, X, X, X
SDTM, assilah, , , , , X, ,
SDTM, el ouamra, X, X, X, X, , X
SDTM, kser lakbir, X, X, X, X, , X
SDTM, arbaoua, X, , , , , ,
SDTM, chewaffaae, , , , , , X
SDTM, dlalha, , , , , , X
SDTM, mly bousselham, , , , , , X
SDTM, lalla mimouna, , , , , , X
SDTM, lemenassera, , , , , , X
SDTM, nador, X, X, X, X, X, X
SDTM, beni nssar, , X, , , , ,
SDTM, tiztoutine, X, , , , , ,
SDTM, driouch, X, , , , , ,
SDTM, midar, X, , , , , ,
SDTM, ben tayeb, X, , , , , ,
SDTM, dar kebdani, X, , , , , ,
SDTM, zghanghan, X, , X, , X, ,
SDTM, selouan, X, , X, , X, ,
SDTM, el araoui, X, , X, , X, ,
SDTM, zaio, , , , , X, ,
SDTM, oujda, X, X, X, X, X, X
SDTM, benidrar, , X, , X, , ,
SDTM, ahfir, , X, , X, , ,
SDTM, saidia, , , , X, , ,
SDTM, sidi moussa lemhaya, X, , , , , ,
SDTM, naima, X, , , , , ,
SDTM, layoun charkiya, X, , , , , ,
SDTM, berkane, X, X, X, X, X, X
SDTM, madagh, X, , , , , ,
SDTM, aklim, X, , , , , ,
SDTM, rabat kamra, X, X, X, X, X, X
SDTM, rabat, X, X, X, X, X, X
SDTM, rabat oecean, X, X, X, X, X, X
SDTM, sale, X, X, X, X, X, X
SDTM, sale el jadida, X, X, X, X, X, X
SDTM, temara, X, X, X, X, X, X
SDTM, ain atik, X, , X, , X, ,
SDTM, skhirate, X, , X, , X, ,
SDTM, tamesna, X, , X, , , ,
SDTM, sidi yahya zaer, X, , X, , , ,
SDTM, ain aouda, X, , X, , , ,
SDTM, aarjate, , X, , , X, ,
SDTM, arjate, , X, , , X, ,
SDTM, sidi allal bahraoui, , X, , , X, ,
SDTM, tifelt, , X, , , X, ,
SDTM, khemisset, , X, , , X, ,
SDTM, khemissat, , X, , , X, ,
SDTM, bouknadel, X, , , , , ,
SDTM, taza, X, X, X, X, X, X,
SDTM, mssoun, X, , X, , X, ,
SDTM, tadart, X, , X, , X, ,
SDTM, guercif, X, , X, , X, ,
SDTM, taourirt, X, , X, , X, ,
SDTM, mkanssa, , , , , , X
SDTM, had ouled zbair, , , , , , X
SDTM, oued amlil, , , , , , X
SDTM, tahla, , , , , , X
SDTM, tanger, X, X, X, X, X, X
SDTM, tanger mghougha, X, X, X, X, X, X
SDTM, tanger centre, X, X, X, X, X, X
SDTM, tanger zone franche, X, , , , , ,
SDTM, meloussa, X, , , , , ,
SDTM, melousa, X, , , , , ,
SDTM, sidi ba kacem, X, , , , , ,
SDTM, haouara, X, , , , , ,
SDTM, ain dalia, X, , , , , ,
SDTM, tetouan, X, X, X, X, X, X
SDTM, dar ben korrich, X, , , , , ,
SDTM, larbaa beni hassan, X, , , , , ,
SDTM, chaoune, X, , , , , ,
SDTM, martil, X, X, X, X, X, X
SDTM, madieq, X, X, X, X, X, ,
SDTM, mdiq, X, X, X, X, X, ,
SDTM, medieq, X, X, X, X, X, ,
SDTM, fnedaq, X, X, X, X, X, ,


LA VOIE EXPRESS, agadir, X, X, X, X, X, X
LA VOIE EXPRESS, ben sergao, X, X, X, X, X, X
LA VOIE EXPRESS, anza, X, , , X, , ,
LA VOIE EXPRESS, aourir, , , , X, , ,
LA VOIE EXPRESS, ait melloul, X, X, X, X, X, X
LA VOIE EXPRESS, inzegane, X, X, X, X, X, X
LA VOIE EXPRESS, ouled teima, , X, , X, X, X
LA VOIE EXPRESS, dcheira, X, X, X, X, X, X
LA VOIE EXPRESS, tikiouine, X, X, X, X, X, X
LA VOIE EXPRESS, laayoune, , , , X, , ,
LA VOIE EXPRESS, tiznit, X, , , , , ,
LA VOIE EXPRESS, guelmim, , , X, , , ,
LA VOIE EXPRESS, taroudante, , , , X, , ,
LA VOIE EXPRESS, biougra, , , X, , , ,
LA VOIE EXPRESS, tantan, , , X, , , ,
LA VOIE EXPRESS, ait baha, , , X, , , ,
LA VOIE EXPRESS, chtouka ait baha, , , X, , , ,
LA VOIE EXPRESS, chtouka ait-baha, , , X, , , ,
LA VOIE EXPRESS, khemis ait amira, , X, , , , ,
LA VOIE EXPRESS, massa, X, , , , , ,
LA VOIE EXPRESS, tarfaya, , , X, , , ,
LA VOIE EXPRESS, bouizakarne, , , X, , , ,
LA VOIE EXPRESS, kleaa, X, X, X, X, X, X
LA VOIE EXPRESS, beni mellal, X, X, X, X, X, X
LA VOIE EXPRESS, khouribga, X, X, X, X, X, X
LA VOIE EXPRESS, fkih ben saleh, X, X, X, X, X, X
LA VOIE EXPRESS, ben hmad, X, , , , , X
LA VOIE EXPRESS, souk sebt, X, X, X, X, X, ,
LA VOIE EXPRESS, souk sabt, X, X, X, X, X, ,
LA VOIE EXPRESS, khenifra, X, , , , , ,
LA VOIE EXPRESS, kasbat tadla, X, , X, , X, ,
LA VOIE EXPRESS, oued zem, , , X, , , ,
LA VOIE EXPRESS, oued zam, , , X, , , ,
LA VOIE EXPRESS, azilal, , X, , , , ,
LA VOIE EXPRESS, zaouiyat cheikh, X, , , , , ,
LA VOIE EXPRESS, bejaad, , , X, , , ,
LA VOIE EXPRESS, mrirt, X, , , , , ,
LA VOIE EXPRESS, sebt nemma, X, X, X, X, X, ,
LA VOIE EXPRESS, ouled zidouh, , , X, X, X, X
LA VOIE EXPRESS, kssiba, , , X, X, X, X
LA VOIE EXPRESS, oued afourar, , X, , , , ,
LA VOIE EXPRESS, boujniba, , , X, , , ,
LA VOIE EXPRESS, tlat oulad, X, , , , , ,
LA VOIE EXPRESS, tighssaline, X, , , , , ,
LA VOIE EXPRESS, ouled ayad, , , X, X, X, X
LA VOIE EXPRESS, ouaouizerth, , X, , , , ,
LA VOIE EXPRESS, ait ishaq, X, , , , , ,
LA VOIE EXPRESS, ouled mrah, , , X, X, X, X
LA VOIE EXPRESS, had bradia, , X, X, X, X, X
LA VOIE EXPRESS, bir mezoui, , , X, , , ,
LA VOIE EXPRESS, oulad mbarek, X, X, X, X, X, X
LA VOIE EXPRESS, foum oudi, X, X, X, X, X, X
LA VOIE EXPRESS, casablanca, X, X, X, X, X, X
LA VOIE EXPRESS, mohammedia, X, X, X, X, X, X
LA VOIE EXPRESS, berrechid, X, X, X, X, X, X
LA VOIE EXPRESS, settat, X, X, X, X, X, X
LA VOIE EXPRESS, bouskoura, X, X, X, X, X, X
LA VOIE EXPRESS, had soualem, X, X, X, X, X, X
LA VOIE EXPRESS, nouasser, X, X, X, X, X, X
LA VOIE EXPRESS, nouaceur, X, X, X, X, X, X
LA VOIE EXPRESS, ain sebaa, X, X, X, X, X, X
LA VOIE EXPRESS, tit mellil, X, X, X, X, X, X
LA VOIE EXPRESS, lekhyayta, X, X, X, X, X, X
LA VOIE EXPRESS, ben slimane, , X, , X, , ,
LA VOIE EXPRESS, ain harrouda, X, X, X, X, X, X
LA VOIE EXPRESS, el gara, , , , , , X
LA VOIE EXPRESS, gara, , , , , , X
LA VOIE EXPRESS, el jadida, X, X, X, X, X, X
LA VOIE EXPRESS, azemmour, X, , X, , X, ,
LA VOIE EXPRESS, sidi bennour, X, , X, , X, ,
LA VOIE EXPRESS, bir jdid, , , , , , X
LA VOIE EXPRESS, khemiss zemamra, X, , X, , X, ,
LA VOIE EXPRESS, oualidia, , , , , X, ,
LA VOIE EXPRESS, sidi smail, X, , X, , X, ,
LA VOIE EXPRESS, fes, X, X, X, X, X, X,
LA VOIE EXPRESS, midelt, , , , X, , ,
LA VOIE EXPRESS, sefrou, , , , , X, ,
LA VOIE EXPRESS, ain taoujtate, X, , , , , ,
LA VOIE EXPRESS, errachidia, , , , X, , ,
LA VOIE EXPRESS, immouzer, , , , X, , ,
LA VOIE EXPRESS, azrou, , , , X, , ,
LA VOIE EXPRESS, immouzer, , , , X, , ,
LA VOIE EXPRESS, ifrane, , , , X, , ,
LA VOIE EXPRESS, arfoud, , , , X, , ,
LA VOIE EXPRESS, rich, , , , X, , ,
LA VOIE EXPRESS, boumia, , , , X, , ,
LA VOIE EXPRESS, taounate, , , , , , X,
LA VOIE EXPRESS, missour, , , , X, , ,
LA VOIE EXPRESS, kariat ba mhamed, , , , , , X,
LA VOIE EXPRESS, boulmane, , , , X, , ,
LA VOIE EXPRESS, goulmima, , , , X, , ,
LA VOIE EXPRESS, outat el haj, , , , X, , ,
LA VOIE EXPRESS, rissani, , , , X, , ,
LA VOIE EXPRESS, tissa, , , , , , X,
LA VOIE EXPRESS, immouzer, , , , , , X,
LA VOIE EXPRESS, zaida, , , , X, , ,
LA VOIE EXPRESS, kenitra, X, X, X, X, X, X,
LA VOIE EXPRESS, sidi kacem, X, , X, , X, ,
LA VOIE EXPRESS, sidi yahia gharb, X, , X, , X, ,
LA VOIE EXPRESS, sidi slimane, X, , X, , X, ,
LA VOIE EXPRESS, mechraa bel ksiri, X, , X, , X, ,
LA VOIE EXPRESS, belksiri, X, , X, , X, ,
LA VOIE EXPRESS, jorf el melha, X, , X, , X, ,
LA VOIE EXPRESS, souk tlet gharb, X, , X, , X, ,
LA VOIE EXPRESS, dar el gueddari, X, , X, , X, ,
LA VOIE EXPRESS, el mudzine, X, , X, , X, ,
LA VOIE EXPRESS, larache, X, X, X, X, X, X,
LA VOIE EXPRESS, ksar el kebir, X, X, X, X, , ,
LA VOIE EXPRESS, laouamra, X, X, X, X, , X
LA VOIE EXPRESS, souk larbaa, X, , , X, , ,
LA VOIE EXPRESS, asilah, , X, , , , ,
LA VOIE EXPRESS, moulay bousselham, X, X, X, , X, ,
LA VOIE EXPRESS, ouazzane, , , X, , , ,
LA VOIE EXPRESS, chefchaouen, , , X, , , ,
LA VOIE EXPRESS, lala mimouna, , X, , X, , ,
LA VOIE EXPRESS, kmiss essahel, , X, , , , ,
LA VOIE EXPRESS, ouazzane, X, X, X, , X, X
LA VOIE EXPRESS, aarbaoua, , X, , , X, ,
LA VOIE EXPRESS, had kourt, , , , X, , ,
LA VOIE EXPRESS, marrakech, X, X, X, X, X, X
LA VOIE EXPRESS, ouazzane, X, , , , , ,
LA VOIE EXPRESS, ouarzazate, X, , , , , ,
LA VOIE EXPRESS, kelaat sraghna, , , , X, , ,
LA VOIE EXPRESS, tinghir, X, , , , , ,
LA VOIE EXPRESS, chichaoua, , , , , X, ,
LA VOIE EXPRESS, ben guerir, , , , X, , ,
LA VOIE EXPRESS, ait ourir, , , , , , X
LA VOIE EXPRESS, attaouia, , , , X, , ,
LA VOIE EXPRESS, zagoura, X, , , , , ,
LA VOIE EXPRESS, kelaat megouna, X, , , , , ,
LA VOIE EXPRESS, amzmiz, X, , , , , ,
LA VOIE EXPRESS, tinjdad, X, , , , , ,
LA VOIE EXPRESS, demnate, X, , , , , ,
LA VOIE EXPRESS, imintanoute, , , , , X, ,
LA VOIE EXPRESS, meknes, X, X, X, X, X, X
LA VOIE EXPRESS, boufekrane, X, X, X, X, X, X
LA VOIE EXPRESS, tifelt, X, , , , , ,
LA VOIE EXPRESS, khemisset, X, , , , , ,
LA VOIE EXPRESS, el hajeb, , , X, , , ,
LA VOIE EXPRESS, ouislane, X, X, X, X, X, X
LA VOIE EXPRESS, oulmes, X, , , , , ,
LA VOIE EXPRESS, moulay driss zerhoun, , , , , X, ,
LA VOIE EXPRESS, my driss zerhoun, , , , , X, ,
LA VOIE EXPRESS, nador, X, X, X, X, X, X
LA VOIE EXPRESS, mont aroui, X, X, X, X, X, X
LA VOIE EXPRESS, selouane, X, X, X, X, X, X
LA VOIE EXPRESS, el hoceima, , , , X, , ,
LA VOIE EXPRESS, driouch, , X, , , , ,
LA VOIE EXPRESS, imzouren, , , , X, , ,
LA VOIE EXPRESS, midar, , X, , , , ,
LA VOIE EXPRESS, beni nsar, , , , , X, ,
LA VOIE EXPRESS, zaio, , , , , , X
LA VOIE EXPRESS, targuist, X, , , , , ,
LA VOIE EXPRESS, ben tayeb, , X, , , , ,
LA VOIE EXPRESS, kariat arekman, , , , , , X
LA VOIE EXPRESS, zghenghen, X, X, X, X, X, X
LA VOIE EXPRESS, kariat arkmane, , , , , , X
LA VOIE EXPRESS, beni bouayach, , , , X, , ,
LA VOIE EXPRESS, beni hdifa, X, , , , , ,
LA VOIE EXPRESS, issaguen, X, , , , , ,
LA VOIE EXPRESS, ketama, X, , , , , ,
LA VOIE EXPRESS, oujda, X, X, X, X, X, X
LA VOIE EXPRESS, layoun, , X, , , , ,
LA VOIE EXPRESS, laayoune, , X, , , , ,
LA VOIE EXPRESS, laayoun, , X, , , , ,
LA VOIE EXPRESS, berkane, X, , X, , X, ,
LA VOIE EXPRESS, ahfir, X, , X, , X, ,
LA VOIE EXPRESS, saidia, , , X, , , ,
LA VOIE EXPRESS, jerada, , , , X, , ,
LA VOIE EXPRESS, rabat, X, X, X, X, X, X
LA VOIE EXPRESS, sale, X, X, X, X, X, X
LA VOIE EXPRESS, temara, X, X, X, X, X, X
LA VOIE EXPRESS, bouznika, X, , , X, , ,
LA VOIE EXPRESS, ain atiq, X, X, X, X, X, X
LA VOIE EXPRESS, skhirat, X, X, X, X, X, X
LA VOIE EXPRESS, ain aouda, X, X, X, X, X, ,
LA VOIE EXPRESS, sidi allal bahraoui, X, , , , , ,
LA VOIE EXPRESS, roumani, , , , , , X
LA VOIE EXPRESS, sidi yahya zaer, X, X, X, X, X, ,
LA VOIE EXPRESS, safi, X, X, X, X, X, X
LA VOIE EXPRESS, essaouira, X, , , , , ,
LA VOIE EXPRESS, youssoufia, , , X, , , ,
LA VOIE EXPRESS, jemaa shaim, , , X, , , ,
LA VOIE EXPRESS, sebt gzoula, X, , , , , ,
LA VOIE EXPRESS, chemaia, , , X, , , ,
LA VOIE EXPRESS, tanger, X, X, X, X, X, X
LA VOIE EXPRESS, tanger med, X, X, X, X, X, X
LA VOIE EXPRESS, taza, X, X, X, X, X, X
LA VOIE EXPRESS, guercif, X, X, X, X, X, X
LA VOIE EXPRESS, taourirt, X, , , , , ,
LA VOIE EXPRESS, tahla, X, , , , , ,
LA VOIE EXPRESS, oued amlil, X, , , , , ,
LA VOIE EXPRESS, tetouan, X, X, X, X, X, X
LA VOIE EXPRESS, fnideq, X, X, X, X, , X
LA VOIE EXPRESS, mediaq, X, X, X, X, , X
LA VOIE EXPRESS, martil, X, X, X, X, , ,
LA VOIE EXPRESS, had beni rzine, X, , , , , ,

"""
# Parse CTM data
rows = data.split('\n')
for row in rows:
    if row.startswith('CTM'):
        parts = row.split(', ')
        dest = parts[1]
        days = [i for i, day in enumerate(parts[2:]) if day=='X']
        carriers[dest] = {'CTM': days}
        
# Parse SDTM data
for row in rows:
    if row.startswith('SDTM'):
        parts = row.split(', ')
        dest = parts[1]
        days = [i for i, day in enumerate(parts[2:]) if day=='X']
        if dest in carriers:
            carriers[dest]['SDTM'] = days
        else:
            carriers[dest] = {'SDTM': days}
            

# Parse LA VOIE EXPRESS data            
for row in rows:
    if row.startswith('LA VOIE EXPRESS'):
        parts = row.split(', ')
        dest = parts[1]
        days = [i for i, day in enumerate(parts[2:]) if day=='X']
        if dest in carriers:
            carriers[dest]['LA VOIE EXPRESS'] = days
        else:
            carriers[dest] = {'LA VOIE EXPRESS': days}
   
@app.route('/')

def home():
    return render_template('app.html')
    
def trouver_meilleur(ville, jour):

  # Parcourir le dictionnaire carriers
  for transporteur, jours in carriers[ville].items():
    
    # Vérifier si le jour est dans la liste
    if jour in jours:
        
      # Retourner le nom du transporteur
      return transporteur
  
  # Transporteur non trouvé    
  return None 

@app.route('/', methods=['GET','POST'])
def home1():

  if request.method == 'POST':

    ville = request.form['ville']
    jour = request.form['jour']
    
    # Trouver meilleur transporteur    
  transporteur = trouver_meilleur(ville, int(jour))    
  return render_template('app.html', transporteur=transporteur, ville=ville, jour=jour)

@app.route('/best_carrier')
def get_best_carrier():

  ville = request.args.get('ville')
  jour = request.args.get('jour')

  best_carrier = trouver_meilleur(ville, jour)

  response = {
      'ville': ville,
      'jour': jour, 
  }
    
  return jsonify(response)

  
        
# Get best carrier for destination     
if __name__ == "__main__":
    app.run(debug=True)