# ==============================================================================
# Production Rule (Context-Free Grammar) Bahasa Sunda
# ==============================================================================

# Terminal 
TERMINALS = {
   'nomina', 'verba', 'adjektiva', 'numeralia', 'pronomina', 'demonstrativa',
   'interjeksi', 'kataSapaan', 'preposisi', 'adverbia', 'partikelPenegas',
}

grammar = {
    # --------------------------------------------------------------------------
    # I. TOP-LEVEL RULE
    # --------------------------------------------------------------------------
    'Kalimat':[
        ['KalimatUtama', 'Panggentra'],
        ['KalimatUtama']
    ],
    
    'KalimatUtama': [
        ['KalimatPananya'],
        ['KalimatPanitah'],
        ['KalimatRangkepan'],
        ['KalimatSalancar'],
        ['KalimatRingkesan'],
        ['KalimatSingget'],
        ['KalimatEbrehan'],
        ['KalimatAnteban'],
    ],
    # --------------------------------------------------------------------------
    # II. JENIS-JENIS KALIMAT
    # --------------------------------------------------------------------------
    # 1. KALIMAT SALANCAR (diwangun ku hiji klausa) 
    'KalimatSalancar': [
        ['KalimatJembar'],
        ['KalimatBasajan'],
    ],

    # Kalimat Basajan (diwangun ku unsur fungsional wajib)
    'KalimatBasajan':[
        ['Klausa']
    ],
    
    'Klausa': [
        ['Subjek', 'Predikat', 'Komplemen', 'Objek'],        # Pola S-P-Kom-O 
        ['Subjek', 'Predikat', 'Objek'],                     # Pola S-P-O 
        ['Subjek', 'Predikat', 'Komplemen'],                 # Pola S-P-Kom 
        ['Predikat', 'Subjek'],                              # Pola Inversi
        ['Subjek', 'Predikat'],                              # Pola S-P
    ],


    # Kalimat Jembar (diwangun ku unsur wajib jeung wenang/keterangan) 
    'KalimatJembar': [
        ['Keterangan', 'KalimatBasajan', 'Keterangan'],
        ['KalimatBasajan', 'Keterangan'],
        ['Keterangan', 'KalimatBasajan'],
        ['KalimatBasajan', 'KeteranganModalitas']
    ],

    # 2. KALIMAT RANGKEPAN (diwangun ku dua klausa atawa leuwih)
    'KalimatRangkepan': [
        ['KalimahNgantet'],
        ['KalimahSumeler']
    ],

    # Kalimah Ngantét (Koordinatif) 
    'KalimahNgantet': [
        ['KalimahNgantetJumlah'], 
        ['KalimahNgantetLalawanan'],
        ['KalimahNgantetPilih'],
        ['KalimahNgantetTumuluy'],
        ['KalimahNgantetSinambung'],
        ['KalimahNgantetPanandes']
    ],

    'KalimahNgantetJumlah': [['Klausa', 'KonjungsiJumlah', 'Klausa']],
    'KalimahNgantetLalawanan': [['Klausa', 'KonjungsiLalawanan', 'Klausa']],
    'KalimahNgantetPilih': [['Klausa', 'KonjungsiPilih', 'Klausa'], ['KonjungsiPilihBerpasangan', 'Klausa', 'KonjungsiPilihBerpasangan', 'Klausa']],
    'KalimahNgantetTumuluy': [['Klausa', 'KonjungsiTumuluy', 'Klausa'], ['KonjungsiWaktu', 'Klausa', 'KonjungsiTumuluy', 'Klausa']],
    'KalimahNgantetSinambung': [['KonjungsiSinambung', 'Klausa', 'KonjungsiSinambung', 'Klausa']],
    'KalimahNgantetPanandes': [['Klausa', 'KonjungsiPanandes', 'Klausa']],
    
    # Kalimah Sumélér (Subordinatif) 
    'KalimahSumeler': [
        ['KalimahSumelerWaktu'], ['KalimahSumelerSarat'], ['KalimahSumelerTujuan'],
        ['KalimahSumelerSabab'], ['KalimahSumelerAkibat'], ['KalimahSumelerHasil'],
        ['KalimahSumelerNgaku'], ['KalimahSumelerCara'], ['KalimahSumelerGuna'],
        ['KalimahSumelerPertelaan'], ['KalimahSumelerPangeces'], ['KalimahSumelerBabandingan']
    ],

    # Unit dasar pembentuk kalimat rangkepan
    'KlausaLulugu': [['Klausa']],

    'KalimahSumelerWaktu': [['KlausaLulugu', 'KlausaSelerWaktu'], ['KlausaSelerWaktu', 'KlausaLulugu']],
    'KalimahSumelerSarat': [['KlausaLulugu', 'KlausaSelerSarat'], ['KlausaSelerSarat', 'KlausaLulugu']],
    'KalimahSumelerTujuan': [['KlausaLulugu', 'KlausaSelerTujuan']],
    'KalimahSumelerSabab': [['KlausaLulugu', 'KlausaSelerSabab'], ['KlausaSelerSabab', 'KlausaLulugu']],
    'KalimahSumelerAkibat': [['KlausaLulugu', 'KlausaSelerAkibat']],
    'KalimahSumelerHasil': [['KlausaLulugu', 'KlausaSelerHasil'], ['KlausaSelerHasil', 'KlausaLulugu']],
    'KalimahSumelerNgaku': [['KlausaLulugu', 'KlausaSelerNgaku'], ['KlausaSelerNgaku', 'KlausaLulugu']],
    'KalimahSumelerCara': [['KlausaLulugu', 'KlausaSelerCara']],
    'KalimahSumelerPertelaan': [['KlausaLulugu', 'KlausaSelerPertelaan']],
    'KalimahSumelerPangeces': [['KlausaLulugu', 'KlausaSelerPangeces']],
    'KalimahSumelerGuna': [['KlausaLulugu', 'KlausaSelerGuna'], ['KlausaSelerGuna', 'KlausaLulugu']],
    'KalimahSumelerBabandingan': [['KlausaLulugu', 'KlausaSelerBabandingan']],

    # 3. KALIMAT RINGKESAN & SINGGET
    'KalimatRingkesan':[
        ['KalimatSinggetan'], ['KalimatRuntuyan'], ['KalimatSambungan'], ['KalimatTambahan'], ['KalimatJawaban']
    ],
    'KalimatSinggetan': [['Predikat', 'Objek'], ['Predikat', 'Keterangan'], ['Subjek'], ['Keterangan'], ['Objek']],
    'KalimatRuntuyan': [['KonjungsiKoordinatif', 'Klausa']], # sempalan tina kalimah ngantét
    'KalimatSambungan': [['KonjungsiSubordinatif', 'Klausa']], # sempalan tina kalimah sumélér
    'KalimatTambahan':[['FrasaNomina'], ['FrasaPreposisional'], ['FrasaAdverbial']],
    'KalimatJawaban': [['FrasaNomina'], ['FrasaAdjektiva'], ['FrasaNumeralia'], ['FrasaVerba'], ['enya'], ['henteu']],
    
    'KalimatSingget':[
        ['KalimatSalam'], ['KalimatPanyeluk'], ['KalimatJudul'], ['KalimatInskripsi']
    ],
    'KalimatSalam': [['punten'], ['wilujeng enjing'], ['hatur nuhun'], ['assalamualaikum'], ['kumaha damang']],
    'KalimatPanyeluk': [['interjeksi']],
    'KalimatJudul': [['FrasaNomina']],  
    'KalimatInskripsi': [['FrasaInskripsi', 'Frasa Nomina', 'KlausaSelerPangeces'], ['FrasaInskripsi', 'FrasaNomina']],
    
    'KalimatPananya':[
        ['KecapPananya', 'KalimatUtama'],
        ['KecapPananya', 'FrasaNomina'],
        ['KecapPananya'],
        ['Klausa', 'KecapPananya'],
    ],

    'KalimatPanitah':[
        ['KalimatParentah'],
        ['KalimatPangajak'],
        ['KalimatPanyarek'],
    ],
    
    'KalimatParentah':[
        ['KecapPanganteurParentah', 'FrasaVerba', 'FrasaNomina'],
        ['KecapPanganteurParentah', 'FrasaVerba'],
        ['FrasaVerba', 'FrasaNomina'],
        ['FrasaVerba'],
    ],

    'KalimatPangajak':[
        ['hayu', 'urang', 'FrasaVerba'],
        ['urang', 'FrasaVerba', 'yu'],
    ],

    'KalimatPanyarek':[
        ['KecapPanyarek', 'Klausa'],
        ['KecapPanyarek', 'FrasaVerba'],
    ],

    'KalimatEbrehan':[
        ['ku', 'FrasaAdjektiva', 'FrasaNomina'],
        ['aya ku', 'FrasaAdjektiva', 'FrasaNomina'],
        ['teuing ku', 'FrasaAdjektiva', 'FrasaNomina'],
    ],

    'KalimatAnteban':[
        ['nya', 'FrasaNomina', 'pisan', 'nu', 'FrasaVerba'],
        ['nya', 'pronomina', 'pisan', 'nu', 'FrasaVerba'],
    ],
    # --------------------------------------------------------------------------
    # III. UNSUR FUNGSIONAL KALIMAT 
    # --------------------------------------------------------------------------
    'Subjek': [['FrasaNomina'], ['pronomina'], ['KlausaSelerPertelaan']],      # Jejer 
    'Predikat': [                                           # Caritaan
        ['FrasaVerba'], 
        ['FrasaAdjektiva'], 
        ['FrasaNumeralia'], 
        ['FrasaNomina'], 
        ['FrasaPreposisional']
    ],
    'Objek': [['FrasaNomina'], ['pronomina'], ['KlausaSelerPertelaan']],                             # Udagan 
    'Komplemen': [                                          # Panglengkep 
        ['FrasaNomina'], 
        ['FrasaVerba'], 
        ['FrasaAdjektiva'],
        ['KlausaSelerPertelaan']
    ],
    'Panggentra': [
        ['FrasaNomina']
    ],
    'Keterangan': [                                         # Katerangan 
        ['KateranganTempat'],
        ['KateranganWaktu'],
        ['KateranganCara'],
        ['KateranganTujuan'],
        ['KateranganPangbarung'],
        ['KateranganAlat'],
        ['KateranganFrekuensi'],
        ['KateranganBabandingan'],
        ['KateranganSabab'],
        ['KateranganIwal'],
        ['KateranganAspek'],
        ['KateranganModalitas']
    ],

    # --------------------------------------------------------------------------
    # IV. JENIS-JENIS FRASA
    # --------------------------------------------------------------------------
    'Frasa': [
        ['FrasaEndosentrik'],
        ['FrasaEksosentrik']
    ],

    # A. Frasa Endosentrik 
    'FrasaEndosentrik': [
        ['FrasaKoordinatif'],
        ['FrasaApositif'],
        ['FrasaAtributif'],
        # Frasa Objektif/Komplementatif dan Konéktif diwakili struktur S-P-O/Kom
    ],
    
    'FrasaKoordinatif': [ # Unsur-unsurna satata 
        ['FrasaNomina', 'KonjungsiKoordinatif', 'FrasaNomina'],
        ['FrasaVerba', 'KonjungsiKoordinatif', 'FrasaVerba'],
        # ['Frasa', 'KonjungsiKoordinatif', 'Frasa']
    ],

    'FrasaApositif': [ # Unsur kadua ngajelaskeun unsur kahiji, référénsi sarua 
        ['FrasaNomina', 'koma', 'FrasaNomina']
    ],
    'FrasaAtributif': [ # Diwangun ku Puseur (inti) jeung Atribut (pewatas) 
        ['nomina', 'KonjungsiPangeces', 'Klausa'],
        ['nomina', 'adjektiva']
    ],

    # B. Frasa Eksosentrik 
    'FrasaEksosentrik': [
        ['FrasaRelasional']
    ],
    
    'FrasaRelasional': [ # Diwangun ku rélator jeung aksis 
        ['FrasaPreposisional']
    ],

    # --------------------------------------------------------------------------
    # V. Rincian Aturan Frasa 
    # --------------------------------------------------------------------------

    # 1. FRASA BARANG (NOMINAL)
    'FrasaNomina': [
        ['FrasaNominaPamungkir'],
        ['FrasaNominaMilik2'], 
        ['FrasaNominaBahan'],
        ['FrasaNominaAsal'], 
        ['FrasaNominaHasil'], 
        ['FrasaNominaSesebutan'], 
        ['FrasaNominaPanangtu1'], 
        ['FrasaNominaMilik1'],
        ['nomina', 'nomina'], 
        ['FrasaVerbaNominal'],
        ['FrasaNominaJumlah'], 
        ['FrasaNominaPamilih1'], 
        ['FrasaNominaPamilih2'], 
        ['FrasaBarangSasaruaan'], 
        ['FrasaNominaPangjentre'], 
        ['FrasaNominaTujuan'], 
        ['FrasaNominaPanangtu2'],
        ['nomina'], 
    ],

    'FrasaNominaJumlah': [['nomina', 'KonjungsiJumlah', 'nomina']], 
    'FrasaNominaPamilih1': [['nomina', 'atawa', 'nomina']], 
    'FrasaNominaPamilih2': [['boh', 'nomina', 'boh', 'nomina']], 
    'FrasaBarangSasaruaan': [['nomina', 'atawa', 'nomina'], ['nomina', 'koma', 'nomina']], 
    'FrasaNominaPangjentre': [['nomina', 'partikelNu', 'FrasaVerba'], ['nomina', 'partikelNu', 'FrasaAdjektiva']],
    'FrasaNominaMilik1': [['nomina', 'pronomina'], ['nomina', 'klitikNa', 'nomina'], ['nomina', 'partikelNu', 'nomina']], 
    'FrasaNominaMilik2': [['partikelNu', 'nomina'], ['bogana', 'nomina']], 
    'FrasaNominaTujuan': [['nomina', 'KonjungsiTujuan', 'FrasaVerba']], 
    'FrasaNominaBahan': [['nomina', 'tina', 'nomina']], 
    'FrasaNominaAsal': [['nomina', 'buatan', 'nomina']], 
    'FrasaNominaPanangtu1': [['nomina', 'demonstrativa'], ['nomina', 'partikelPenegas']], 
    'FrasaNominaPanangtu2': [['partikelNu', 'FrasaVerba'], ['partikelNu', 'FrasaAdjektiva']], 
    'FrasaNominaHasil': [['nomina', 'hasil', 'nomina']], 
    'FrasaNominaSesebutan': [['kataSapaan', 'nomina']], 
    'FrasaNominaPamungkir': [['lain', 'FrasaNomina']], 
    'FrasaVerbaNominal': [['FrasaVerba', 'partikelPenegas']], # nominalisasi 

    # 2. FRASA PAGAWÉAN (VERBAL) 
    'FrasaVerba': [
        ['FrasaVerbaPamungkir'], 
        ['FrasaVerbaAspek'], 
        ['FrasaVerbaModalitas'],
        ['verba', 'verba'], 
        ['FrasaVerbaJumlah'], 
        ['FrasaVerbaPamilih1'], 
        ['FrasaVerbaPamilih2'],
        ['verba'], 
    ],

    'FrasaVerbaJumlah': [['verba', 'jeung', 'verba']], 
    'FrasaVerbaPamilih1': [['verba', 'atawa', 'verba']], 
    'FrasaVerbaPamilih2': [['boh', 'verba', 'boh', 'verba']], 
    'FrasaVerbaPamungkir': [['KonjungsiPamungkirVerbal', 'verba']], 
    'FrasaVerbaAspek': [['KecapAspek', 'verba']],
    'FrasaVerbaModalitas': [['KecapModalitas', 'verba']],

    # 3. FRASA SIPAT (ADJEKTIVAL) 
    'FrasaAdjektiva': [
        ['FrasaAdjektivaTingkat3'],
        ['FrasaAdjektivaTingkat2'], 
        ['FrasaAdjektivaTingkat1'], 
        ['FrasaAdjektivaUndak'], 
        ['FrasaAdjektivaPamungkir'], 
        ['FrasaAdjektivaAspek'],
        ['FrasaAdjektivaJumlah'], 
        ['FrasaAdjektivaPamilih1'], 
        ['FrasaAdjektivaPamilih2'],
        ['adjektiva'], 
    ],

    'FrasaAdjektivaJumlah': [['adjektiva', 'KonjungsiJumlah', 'adjektiva']], 
    'FrasaAdjektivaPamilih1': [['adjektiva', 'atawa', 'adjektiva']], 
    'FrasaAdjektivaPamilih2': [['boh', 'adjektiva', 'boh', 'adjektiva']], 
    'FrasaAdjektivaTingkat1': [['PangantebTingkat1', 'adjektiva'], ['adjektiva', 'PangantebTingkat1']], 
    'FrasaAdjektivaTingkat2': [['PangantebTingkat2', 'adjektiva']], 
    'FrasaAdjektivaTingkat3': [['PangantebTingkat3', 'adjektiva', 'klitikNa']],
    'FrasaAdjektivaUndak': [['PangantebUndak', 'adjektiva']], 
    'FrasaAdjektivaPamungkir': [['KonjungsiPamungkirVerbal', 'adjektiva']], 
    'FrasaAdjektivaAspek': [['KecapAspek', 'adjektiva']], 

    # 4. FRASA BILANGAN (NUMERAL) 
    'FrasaNumeralia': [
        ['numeralia'], ['FrasaNumeraliaTitikelan'], ['FrasaNumeraliaJumlah'], ['FrasaNumeraliaPamilih'],
        ['FrasaNumeraliaWates'], ['FrasaNumeraliaAspek'], ['FrasaNumeraliaPamungkir']
    ],

    'FrasaNumeraliaTitikelan': [['numeralia', 'nomina']], 
    'FrasaNumeraliaJumlah': [['numeralia', 'jeung', 'numeralia']], 
    'FrasaNumeraliaPamilih': [['numeralia', 'atawa', 'numeralia']], 
    'FrasaNumeraliaWates': [['PangantebWates', 'numeralia']], 
    'FrasaNumeraliaAspek': [['KecapAspek', 'numeralia']], 
    'FrasaNumeraliaPamungkir': [['KonjungsiPamungkirNumeral', 'numeralia']], 
    
    # 5. FRASA PANGANTÉT (PREPOSISIONAL) 
    'FrasaPreposisional': [
        ['preposisi', 'EntitasTempat'],
        ['preposisi', 'FrasaNomina'],
    ],

    'FrasaAdverbial':[
        ['adverbia']
    ],

    'EntitasTempat':[
        ['nomina'],
        ['nomina', 'nomina'],
        ['nomina', 'nomina', 'nomina']
    ],

    'FrasaInskripsi':[['keur'], ['kanggo'], ['haturan'], ['kahatur'], ['katresna kanggo'], ['tawis asih ka'], ['tawis soca kanggo'], ['tawis katineung kanggo'], ['tawis baktos kanggo'], ['kanyaah ka'], ['sungkeman kanggo']],

     # --------------------------------------------------------------------------
    # VI. Aturan Keterangan 
    # --------------------------------------------------------------------------
    'KateranganTempat': [['PreposisiTempat', 'FrasaNomina'], ['PreposisiTempat', 'EntitasTempat']], 
    'KateranganWaktu': [['FrasaAdverbial'], ['FrasaNominaWaktu'], ['PreposisiWaktu', 'FrasaNominaWaktu']], 
    'KateranganCara': [['adjektiva'], ['kalawan', 'adjektiva'], ['bari', 'Klausa']], 
    'KateranganTujuan': [['PreposisiTujuan', 'FrasaNomina']], 
    'KateranganPangbarung': [['jeung', 'FrasaNomina']], 
    'KateranganAlat': [['PreposisiAlat', 'FrasaNomina']], 
    'KateranganFrekuensi': [['FrasaNumeralia', 'kali']], 
    'KateranganBabandingan': [['KecapBabandingan', 'FrasaNomina']], 
    'KateranganSabab': [['PreposisiSabab', 'FrasaNomina']], 
    'KateranganIwal': [['PreposisiIwal', 'FrasaNomina']], 
    'KateranganAspek': [['KecapAspekSpontanitas', 'FrasaVerba']], 
    'KateranganModalitas': [
        ['KecapModalitasKapastian'], ['KecapModalitasKahangham'], ['KecapModalitasKainggis'],
        ['KecapModalitasKawajiban'], ['KecapModalitasPaidin'], ['KecapModalitasPamungkir'],
        ['KecapModalitasKahanjakal'], ['KecapModalitasPangarep'], ['KecapModalitasKaheran']
    ], 

    # --------------------------------------------------------------------------
    # VII. Kelompok Kecap 
    # --------------------------------------------------------------------------
    # Definisi Klausa Sélér Spesifik
    'KlausaSelerWaktu': [['KonjungsiWaktu', 'Klausa']],
    'KlausaSelerSarat': [['KonjungsiSarat', 'Klausa']],
    'KlausaSelerTujuan': [['KonjungsiTujuan', 'Klausa']],
    'KlausaSelerSabab': [['KonjungsiSabab', 'Klausa']],
    'KlausaSelerAkibat': [['KonjungsiAkibat', 'Klausa']],
    'KlausaSelerHasil': [['KonjungsiHasil', 'Klausa']],
    'KlausaSelerNgaku': [['KonjungsiNgaku', 'Klausa']],
    'KlausaSelerCara': [['KonjungsiCara', 'Klausa']],
    'KlausaSelerGuna': [['KonjungsiGuna', 'Klausa']],
    'KlausaSelerBabandingan': [['KonjungsiBabandingan', 'Klausa']],
    'KlausaSelerPertelaan': [['KonjungsiPertelaan', 'Klausa']],
    'KlausaSelerPangeces': [['KonjungsiPangeces', 'Klausa']],
    
    'KonjungsiKoordinatif': [['jeung'], ['tur'], ['atawa']], 
    'KonjungsiSubordinatif': [['sangkan'], ['sabab'], ['waktu'], ['lamun']], 

    'KonjungsiJumlah': [['jeung'], ['katut'], ['tur'], ['sarta'], ['tambah-tambah'], ['turug-turug'], ['sajaba'], ['kitu deui']], 
    'KonjungsiLalawanan': [['tapi'], ['padahal'], ['tapi oge'], ['tapi deuih']],
    'KonjungsiPilih':[['atawa']],
    'KonjungsiPilihBerpasangan': [['teuing'], ['duka']],
    'KonjungsiTumuluy':[['tuluy'], ['terus']],
    'KonjungsiSinambung': [['beuki'], ['tambah'], ['mingkin']],
    'KonjungsiPanandes': [['malah']],
    'KonjungsiWaktu': [['waktu'], ['basa'], ['sabot'], ['memeh'], ['samemeh'], ['bada'], ['sabada'], ['sanggeus'], ['barang'], ['saban'], ['saban-saban'],
                       ['unggal'], ['unggal-unggal'], ['ti barang'], ['ti memeh'], ['ti saprak'], ['nepi ka'], ['salila'], ['sapanjang'], ['sapapadana']],
    'KonjungsiSarat': [['lamun'], ['asal'], ['mun'], ['mun seug'], ['upama'], ['saupama']],
    'KonjungsiTujuan':[['ambeh'], ['ngarah'], ['supaya'], ['sangkan'], ['malar'], ['malahmandar']],
    'KonjungsiSabab': [['saba'], ['lantaran'], ['pedah'], ['alatan'], ['bubuhan'], ['da'], ['dumeh'], ['bakat ku']],
    'KonjungsiAkibat': [['nepi ka']],
    'KonjungsiHasil': [['nu matak'], ['pang'], ['pangna'], ['mana']],
    'KonjungsiNgaku': [['najan'], ['najan kitu'], ['sanajan'], ['sanajan kitu'], ['sok sanajan'], ['papadaning'], ['sangkilang']],
    'KonjungsiCara':[['bari'], ['kalawan'], ['ku jalan']],
    'KonjungsiGuna': [['pikeun'], ['keur']],
    'KonjungsiPertelaan': [['yen'], ['majar'], ['naon'], ['kumaha']],
    'KonjungsiPangeces': [['nu']],
    'KonjungsiBabandingan': [['cara'], ['lir'], ['kawas'], ['siga'], ['jiga'], ['saperti'], ['asa'], ['bangun'], ['batan']],

    'KonjungsiPamungkirVerbal': [['henteu'], ['acan'], ['moal']], 
    'KonjungsiPamungkirNumeral': [['lain'], ['henteu']], 
    'KecapAspek': [
        ['gék'], ['bray'], ['geus'], ['parantos'], ['keur'], ['nuju'], ['bakal'], ['badé'], ['mindeng'], 
        ['kungsi'], ['hantem'], ['teu weléh'], ['ngadadak'], ['deui'], ['biasa'], ['sok']
    ], 
    'KecapModalitas': [
        ['pasti'], ['meureun'], ['bisi'], ['kudu'], ['meunang'], ['piraku'], ['hanas'], ['muga'], ['baruk']
    ], 

    'KecapPananya':[
        ['saha'], ['naon'], ['iraha'], ['kumaha'], ['sabaraha'],
        ['di mana'], ['ka mana'], ['ti mana'], ['naha'], ['ku naon']
    ],

    'KecapPanganteurParentah': [['cing'], ['geura'], ['sina'], ['sing']],
    'KecapPanyarek': [['ulah'], ['tong'], ['entong']],

     # Rincian kecap Keterangan Modalitas 
    'KecapModalitasKapastian': [['pasti'], ['tangtu'], ['moal boa'], ['moal burung'], ['tanwande']],
    'KecapModalitasKahangham': [['meureun'], ['sigana'], ['kawasna'], ['rupina'], ['panginten']],
    'KecapModalitasKainggis': [['palangsiang'], ['boa-boa'], ['bisi'], ['bilih'], ['paur']],
    'KecapModalitasKawajiban': [['kudu'], ['wajib'], ['perlu'], ['kedah'], ['misti']],
    'KecapModalitasPaidin': [['meunang'], ['bisa'], ['tiasa'], ['kengeng']],
    'KecapModalitasPamungkir': [['piraku'], ['moal enya'], ['mustahil']],
    'KecapModalitasKahanjakal': [['hanas'], ['boro']],
    'KecapModalitasPangarep': [['muga'], ['mugi'], ['mugia'], ['mudah-mudahan'], ['muga-muga'], ['mugi-mugi'], ['hayang teh']],
    'KecapModalitasKaheran': [['baruk'], ['kutan'], ['geuning'], ['sihoreng'], ['manahoreng'], ['karah']],

    'PreposisiTempat': [['di'], ['dina'], ['ka'], ['kana'], ['ti'], ['tina']], 
    'PreposisiWaktu': [['ti'], ['nepi ka'], ['dina']],
    'PreposisiTujuan': [['keur'], ['pikeun']], 
    'PreposisiAlat': [['ku'], ['kana'], ['maké']], 
    'PreposisiSabab': [['ku'], ['sabab'], ['lantaran']], 
    'PreposisiIwal': [['iwal'], ['jaba'], ['kajaba']], 
    'KecapBabandingan': [['siga'], ['kawas'], ['batan']], 
    'PangantebTingkat1': [['rada'], ['leuwih'], ['mani'], ['naker'], ['pisan'], ['teuing']], 
    'PangantebTingkat2': [['aya ku'], ['carék ku'], ['teuing ku']], 
    'PangantebTingkat3': [['kacida'], ['pohara']], 
    'PangantebUndak': [['beuki'], ['tambah']], 
    'PangantebWates': [['ngan'], ['ukur']], 

    'partikelNu': [['nu']],
    'klitikNa': [['na']],
    'koma': [[',']],
}