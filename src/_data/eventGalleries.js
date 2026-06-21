function numberedImages({
  folder,
  prefix,
  count,
  label,
  dimensions,
  firstAlt,
  altByNumber = {},
  firstCaption,
}) {
  return Array.from({ length: count }, (_, offset) => {
    const number = offset + 1;
    const size = dimensions(number);

    return {
      src: `/assets/images/events/${folder}/${prefix}-${String(number).padStart(2, "0")}.jpg`,
      alt:
        altByNumber[number] ??
        (number === 1 && firstAlt ? firstAlt : `${label}, fotografi ${number}.`),
      caption: number === 1 ? firstCaption : undefined,
      width: size.width,
      height: size.height,
    };
  });
}

const size = (width, height) => () => ({ width, height });

export default {
  jubileum2017: numberedImages({
    folder: "jubileum-2017",
    prefix: "jubileum-2017",
    count: 39,
    label: "350-årsjubileet for finneinnvandringen i Risberget",
    dimensions: size(2500, 1875),
    firstAlt: "Håndmalt skilt med teksten «350 år» langs veien til jubileet.",
    altByNumber: {
      22: "Besøkende sitter utenfor forsamlingslokalet under 350-årsjubileet.",
    },
  }),
  kulturdag2019: numberedImages({
    folder: "kulturdag-2019",
    prefix: "kulturdag-2019",
    count: 12,
    label: "Kulturdagen 2019 om jakttradisjoner på Finnskogen",
    dimensions: size(2500, 1875),
    firstAlt: "Foredrag om jegerrollen under Kulturdagen 2019.",
  }),
  kulturdag2020: numberedImages({
    folder: "kulturdag-2020",
    prefix: "kulturdag-2020",
    count: 1,
    label: "Kulturdagen 2020",
    dimensions: size(720, 960),
    firstAlt: "Plakat for Kulturdagen 2020 med rød tekst som viser at arrangementet er avlyst.",
    firstCaption: "Arrangementet ble utsatt på grunn av koronapandemien.",
  }),
  kulturdag2021: numberedImages({
    folder: "kulturdag-2021",
    prefix: "kulturdag-2021",
    count: 37,
    label: "Kulturdagen 2021 om Risberget under krig og okkupasjon",
    dimensions: (number) => {
      const sizes = {
        1: { width: 430, height: 243 },
        2: { width: 270, height: 192 },
        3: { width: 960, height: 540 },
        4: { width: 1057, height: 1280 },
        5: { width: 960, height: 1280 },
        37: { width: 809, height: 540 },
      };
      if (sizes[number]) return sizes[number];
      if (number >= 11 && number <= 28) return { width: 175, height: 131 };
      if (number === 29 || number === 30) return { width: 270, height: 202 };
      if (number >= 31 && number <= 36) return { width: 175, height: 131 };
      return { width: 1280, height: 960 };
    },
    firstAlt: "Plakatoverskrift for Kulturdagen i Risberget 11. september 2021.",
    firstCaption: "Temaet var Risberget under krig og okkupasjon.",
  }),
  kulturdag2022: numberedImages({
    folder: "kulturdag-2022",
    prefix: "kulturdag-2022",
    count: 14,
    label: "Kulturdagen 2022 i Risberget",
    dimensions: (number) => {
      if (number === 1) return { width: 1280, height: 948 };
      if (number === 12) return { width: 1280, height: 837 };
      return { width: 1280, height: 960 };
    },
    firstAlt: "Presentasjon med tittelen «Da svedjefinnene kom til Risberget».",
  }),
};
