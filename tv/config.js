/* Boulevard TV — cilësimet. Çmimet NUK shkruhen këtu: merren live nga sistemi (vetëm lexim).
   Këtu zgjedhim VETËM çfarë del në ekran dhe me çfarë emri. */
window.TV_CONFIG = {
  db: {
    url: 'https://c--58dc0c87-3008-4bdc-85e3-82d8c17aeb57-prod.lovable.cloud',
    key: 'sb_publishable_Wq2dUS_Y4EVTcSOQggwBhg_3grIeO_s' // çelës publik (i njëjti që përdor menuja e klientit)
  },
  /* Fotot dhe videot merren nga GitHub (dosja tv/ e projektit). */
  mediaBase: 'https://raw.githubusercontent.com/inventarimenu-star/Prova/main/tv/',
  seconds: 10,          // sa sekonda qëndron çdo ekran
  phone: '067 401 0030',
  timezone: 'Europe/Tirane',

  /* Ekranet, sipas radhës. Një ekran "offer" del VETËM kur oferta është aktive në sistem dhe brenda orarit të saj.
     items: [emri në sistem, emri në TV]. Artikujt që mungojnë ose s'janë në ofertë nuk shfaqen. */
  slides: [
    { type: 'offer', design: true, bg: 'media/bg-mengjesi.jpg', offer: 'Oferta e Mëngjesit', kicker: 'OFERTA E MËNGJESIT', title: 'Fillo ditën me ne', theme: 'gold',
      footer: 'E 10-ta kafe *FALAS* kur porosit nga telefoni', tagline: ['Kafe e mirë,', 'fillim i mbarë!'],
      items: [['KAFE expres', 'Kafe ekspres', 'cup'], ['KAFE MAKIATO', 'Makiato', 'cup'], ['KAPUCHINO ME KAFE', 'Kapuçino', 'cup'],
              ['Briosh', 'Briosh', 'croissant'], ['ÇOKOLLATE', 'Çokollatë', 'choc'], ['CAJ I NXEHTË BIO', 'Çaj bio', 'tea']] },
    { type: 'image', src: 'media/poster-mengjesi.jpg', offer: 'Oferta e Mëngjesit' },   // poster CapCut (del vetëm 07–11)
    { type: 'product', offer: 'Oferta e Mëngjesit', item: 'KAFE expres', label: 'Kafe ekspres', kicker: 'MËNGJESI',
      photo: 'media/espresso.jpg', layout: 'full', theme: 'gold' },

    { type: 'offer', design: true, bg: 'media/bg-dreka.jpg', kickIcon: 'pizza', offer: 'Oferta e Drekës 🍕', kicker: 'OFERTA E DREKËS', title: 'Pizza 100 lekë më lirë', theme: 'orange',
      footer: 'Porosit nga telefoni: skano *QR-në* në tavolinë', tagline: ['Drekë e shijshme,', 'çmim i mirë!'],
      items: [['Pizza Margarita', 'Margarita', 'pizza'], ['Pizza Kapricoza', 'Kapricoza', 'pizza'], ['Pizza Tono', 'Tono', 'pizza'],
              ['Pizza 4 Djatherat', '4 Djathërat', 'pizza'], ['Chicken Wings', 'Chicken Wings', 'wings'], ['Chiken Finger', 'Chicken Finger', 'finger']] },
    { type: 'product', offer: 'Oferta e Drekës 🍕', item: 'Pizza Margarita', label: 'Pizza Margarita', kicker: 'DREKA',
      photo: 'media/food-pizza-clean.jpg', layout: 'side', theme: 'orange' },
    { type: 'video', src: 'media/reel-pizza.mp4', offer: 'Oferta e Drekës 🍕', kicker: 'DREKA', title: 'Pizza e freskët', theme: 'orange' },

    { type: 'offer', design: true, bg: 'media/bg-birra.jpg', kickIcon: 'beer', offer: '🍺 & 🍷', kicker: 'BIRRA & VERË', title: 'Belge premium, çmim Heineken-i', theme: 'green',
      footer: 'Skano QR-në në faturë: mund të jesh *fitues*!', tagline: ['Gëzuar,', 'miq!'],
      items: [['Duvel Beer', 'Duvel', 'beer'], ['Blenche de Namy', 'Blanche', 'beer'], ['HEINEKEN SHISHE 400ml', 'Heineken', 'bottle'],
              ['KRIKO Heineken 400ml', 'Heineken kriko', 'beer'], ['Birra Moretti 330ml', 'Moretti', 'bottle'], ['GOTE VERE', 'Gotë verë', 'wine']] },

    { type: 'video', src: 'media/reel-kafeja.mp4', kicker: 'BOULEVARD CAFFE', title: 'Kafeja jonë', theme: 'gold' },
    { type: 'matches' },
    { type: 'loyalty', active: false },   // fikur: e mbulon posteri i besnikërisë (ndize me true nëse do edhe kartën e lotarisë)
    { type: 'image', src: 'media/poster-besnikeria.jpg', active: true },              // poster CapCut i besnikërisë (QR i vërtetë)
    { type: 'image', src: 'media/poster-kerkon-staf.jpg', active: true },             // poster CapCut: kërkon staf (fike me false kur gjen njeri)
    { type: 'notice', active: false, kicker: 'NJOFTIM', title: 'Kërkojmë kamarier/e', sub: 'Për turnin e parë (mëngjes)',
      pill: 'Aplikoni: 067 401 0030', note: 'Telefononi, shkruani në WhatsApp ose ejani në lokal' }
  ],

  /* Ndeshjet: shfaqen vetëm ditën e shënuar (date = YYYY-MM-DD). */
  matches: {
    date: '2026-10-24',
    offerLine: 'Heineken 200 lekë · shishe ose kriko',
    list: [
      // ['ORA', 'Shtëpia', 'Mysafiri', 'Kampionati']  (stemat merren vetë nga media/logos/)
      ['13:30', 'Aston Villa', 'Man City', 'Premier League'],
      ['13:30', 'Partizani', 'Skënderbeu', 'Abissnet Superiore'],
      ['13:30', 'Laçi', 'Vora', 'Abissnet Superiore'],
      ['16:00', 'Arsenal', 'Everton', 'Premier League'],
      ['18:00', 'Napoli', 'Roma', 'Serie A'],
      ['18:30', 'Teuta', 'AF Elbasani', 'Abissnet Superiore'],
      ['18:30', 'Vllaznia', 'Tirana', 'Abissnet Superiore'],
      ['18:30', 'Chelsea', 'Tottenham', 'Premier League'],
      ['21:00', 'Atlético', 'Deportivo', 'La Liga']
    ]
  },

  /* REKLAMA (biznese të tjera ose të tuat). Del çdo "every" ekrane, vetëm nga "from" deri "to".
     image: foto 16:9 (1920×1080) ose video: 'media/...mp4'. Shembull:
     { name: 'Dyqani X', image: 'media/reklama-dyqani-x.jpg', from: '2026-11-01', to: '2026-11-30', every: 4 } */
  ads: []
};
