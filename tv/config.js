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

    /* Dizajnet e pronarit (24 tetor): sfondi është fotoja e tij; çmimet vendosen live sipër, në vendin e tyre (koordinata në pikselët e fotos 1672×940). */
    { type: 'priced', bg: 'media/design-dreka.jpg', src: 1672, offer: 'Oferta e Drekës 🍕', color: '#F5BE4B',
      prices: [['Pizza Margarita', [528, 403, 654, 443], [445, 420, 509, 445]], ['Pizza Tono', [533, 530, 659, 571], [447, 548, 510, 573]],
               ['Chicken Wings', [534, 672, 659, 712], [445, 691, 511, 716]], ['Pizza Kapricoza', [1204, 407, 1330, 448], [1120, 423, 1183, 448]],
               ['Pizza 4 Djatherat', [1207, 545, 1334, 586], [1121, 561, 1184, 586]], ['Chiken Finger', [1209, 683, 1335, 723], [1130, 693, 1190, 718]]] },
    { type: 'image', src: 'media/design-antipaste.jpg', from: '12:00', to: '18:00' },   // Antipaste, pa çmim, vetëm 12–18

    { type: 'priced', bg: 'media/design-birra.jpg', src: 1672, offer: '🍺 & 🍷', color: '#F5BE4B',
      prices: [['Duvel Beer', [515, 458, 601, 487]], ['HEINEKEN SHISHE 400ml', [515, 564, 601, 592]], ['Birra Moretti 330ml', [515, 675, 602, 703]],
               ['Blenche de Namy', [1041, 458, 1127, 487]], ['KRIKO Heineken 400ml', [1045, 565, 1132, 593]], ['GOTE VERE', [1052, 677, 1134, 705]]] },
    { type: 'video', design: true, bg: 'media/bg-heineken.jpg', src: 'media/reel-heineken.mp4', offer: '🍺 & 🍷', kickIcon: 'beer',
      kicker: 'BIRRA & VERË · 12:00–23:00', title: 'Heineken', priceItem: 'HEINEKEN SHISHE 400ml', priceText: '{p} lekë · shishe ose kriko',
      footer: 'Skano QR-në në faturë: mund të jesh *fitues*!' },

    { type: 'video', design: true, bg: 'media/bg-mengjesi.jpg', src: 'media/reel-kafeja.mp4', kicker: 'ESPRESSO · KAPUÇINO · MAKIATO', title: 'Kafeja jonë', theme: 'gold',
      footer: 'E 10-ta kafe *FALAS* kur porosit nga telefoni', tagline: ['Kafe e mirë,', 'fillim i mbarë!'] },
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
