import React, { useId, type ReactNode } from "react";

// A fixed portrait grammar taken from wishy-cat.jpg. These are authored designs,
// not a family index plus a scale multiplier. Coordinates stay in a 256px square.
export const catInk = "#17101f";
const white = "#fffdf7",
  gold = "#f8bc19",
  rose = "#f2a1b7",
  mint = "#8bd4bf",
  lilac = "#c5a7f0";
const line = {
  stroke: catInk,
  strokeWidth: 3.2,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};
const p = (d: string, fill = "none", width = 2.4) => (
  <path d={d} fill={fill} {...line} strokeWidth={width} />
);
const c = (x: number, y: number, r: number, fill = white) => (
  <circle cx={x} cy={y} r={r} fill={fill} />
);
const e = (x: number, y: number, rx: number, ry: number, fill = white) => (
  <ellipse cx={x} cy={y} rx={rx} ry={ry} fill={fill} />
);
const g = (...children: ReactNode[]) =>
  React.createElement("g", null, ...children);
const mirror = (art: ReactNode) =>
  g(art, <g transform="translate(256 0) scale(-1 1)">{art}</g>);
const star = (x: number, y: number, fill = gold) => (
  <path
    d="M0 -8 2 -2 8 0 2 2 0 8 -2 2 -8 0 -2 -2Z"
    transform={`translate(${x} ${y})`}
    fill={fill}
  />
);
const heart = (x: number, y: number, fill = rose) => (
  <path
    d="M0 6 C-16 -3 -5 -12 0 -5 C5 -12 16 -3 0 6Z"
    transform={`translate(${x} ${y})`}
    fill={fill}
  />
);
const leaf = (x: number, y: number, fill = mint) =>
  g(
    p(`M${x} ${y} q-13 -17 1 -22 q13 14 -1 22Z`, fill, 1.8),
    p(`M${x} ${y} v-14`, "none", 1.5),
  );
export type CatDesign = { name: string; fa: string; art: ReactNode };
const d = (name: string, fa: string, art: ReactNode): CatDesign => ({
  name,
  fa,
  art,
});
function FaceSilhouette({
  outline,
  detail,
}: {
  outline: string;
  detail?: ReactNode;
}) {
  const id = `contour-${useId().replace(/[^a-zA-Z0-9_-]/g, "")}`;
  // Hide the artificial line where a separately selected ear joins the head.
  // The central forehead and lower cheek silhouette keep the original outline.
  return (
    <g>
      <defs>
        <clipPath id={id}>
          <path d="M88 0 H168 V119 H256 V256 H0 V119 H88Z" />
        </clipPath>
      </defs>
      {p(outline, "currentColor", 0)}
      <g clipPath={`url(#${id})`}>{p(outline, "none", 3.8)}</g>
      {detail}
    </g>
  );
}
const face = (
  name: string,
  fa: string,
  outline: string,
  detail?: ReactNode,
) => ({
  ...d(name, fa, <FaceSilhouette outline={outline} detail={detail} />),
  outline,
});
export const faceDesigns = [
  face(
    "Wishy",
    "ویشی",
    "M43 121 Q37 88 72 77 Q128 52 184 77 Q219 88 213 121 Q228 130 231 146 Q220 142 215 146 L226 157 214 157 Q199 221 128 224 Q57 221 42 157 L30 157 41 146 Q36 142 25 146 Q28 130 43 121Z",
  ),
  face(
    "Cloud cheeks",
    "گونه‌ابری",
    "M44 119 Q39 76 88 74 Q128 60 168 74 Q217 76 212 119 Q230 119 225 137 Q241 147 222 158 Q224 178 207 178 Q184 220 128 222 Q72 220 49 178 Q32 178 34 158 Q15 147 31 137 Q26 119 44 119Z",
  ),
  face(
    "Mochi",
    "موچی",
    "M39 117 Q37 73 83 72 Q128 61 173 72 Q219 73 217 117 L220 161 Q217 219 128 220 Q39 219 36 161Z",
  ),
  face(
    "Little lynx",
    "سیاه‌گوش",
    "M43 117 Q41 78 89 74 Q128 64 167 74 Q215 78 213 117 L225 130 217 136 231 149 216 154 222 167 206 170 Q191 215 128 224 Q65 215 50 170 L34 167 40 154 25 149 39 136 31 130Z",
  ),
  face(
    "Peach chin",
    "چونه‌هلو",
    "M42 117 Q40 75 86 75 Q128 62 170 75 Q216 75 214 117 Q224 166 195 191 Q164 217 143 215 Q128 231 113 215 Q92 217 61 191 Q32 166 42 117Z",
  ),
  face(
    "Buttercup",
    "آلاله",
    "M43 118 Q42 77 87 75 Q128 63 169 75 Q214 77 213 118 Q228 134 218 154 Q224 174 201 183 Q191 210 165 211 Q145 228 128 218 Q111 228 91 211 Q65 210 55 183 Q32 174 38 154 Q28 134 43 118Z",
  ),
  face(
    "Fox fluff",
    "پشمکی",
    "M44 120 Q36 78 89 74 Q128 62 167 74 Q220 78 212 120 L229 139 215 143 225 158 211 158 217 174 199 179 Q170 218 128 225 Q86 218 57 179 L39 174 45 158 31 158 41 143 27 139Z",
  ),
  face(
    "Dumpling",
    "پیراشکی",
    "M41 118 Q39 73 82 72 Q128 58 174 72 Q217 73 215 118 Q228 145 216 178 Q199 214 158 220 H98 Q57 214 40 178 Q28 145 41 118Z",
    p("M110 214 Q128 219 146 214", "none", 1.4),
  ),
  face(
    "Soft square",
    "چهارگوش نرم",
    "M42 113 Q42 76 80 76 Q128 62 176 76 Q214 76 214 113 V176 Q214 216 174 218 H82 Q42 216 42 176Z",
  ),
  face(
    "Heart cheeks",
    "صورت‌قلبی",
    "M42 118 Q40 75 79 73 Q110 65 128 78 Q146 65 177 73 Q216 75 214 118 Q225 163 197 187 Q170 207 128 226 Q86 207 59 187 Q31 163 42 118Z",
  ),
  face(
    "Crescent chin",
    "چونه‌هلالی",
    "M42 120 Q36 78 84 74 Q128 59 172 74 Q220 78 214 120 Q228 163 195 194 Q163 226 128 220 Q93 226 61 194 Q28 163 42 120Z",
    p("M113 212 Q128 216 143 212", "none", 1.4),
  ),
  face(
    "Cheek tassels",
    "گونه‌منگوله‌ای",
    "M43 117 Q40 76 85 74 Q128 62 171 74 Q216 76 213 117 L223 134 218 139 229 151 219 155 225 169 210 167 205 181 Q181 219 128 223 Q75 219 51 181 L46 167 31 169 37 155 27 151 38 139 33 134Z",
  ),
  face(
    "Pear",
    "گلابی",
    "M46 118 Q41 75 90 74 Q128 64 166 74 Q215 75 210 118 Q235 165 207 193 Q177 221 128 223 Q79 221 49 193 Q21 165 46 118Z",
  ),
  face(
    "Marshmallow",
    "مارشملو",
    "M42 119 Q37 83 76 77 Q98 65 128 73 Q158 65 180 77 Q219 83 214 119 Q227 141 219 160 Q228 189 201 203 Q174 224 128 219 Q82 224 55 203 Q28 189 37 160 Q29 141 42 119Z",
  ),
  face(
    "Topknot",
    "کاکلی",
    "M42 121 Q37 80 83 77 L101 62 108 74 127 56 134 72 151 64 167 76 Q219 80 214 121 Q229 163 201 190 Q176 220 128 224 Q80 220 55 190 Q27 163 42 121Z",
  ),
  face(
    "Double tuft",
    "دوکاکلی",
    "M43 119 Q40 82 82 76 L95 62 106 74 118 63 128 76 138 63 150 74 161 62 174 76 Q216 82 213 119 Q229 165 198 195 Q169 224 128 221 Q87 224 58 195 Q27 165 43 119Z",
  ),
  face(
    "Bean cheeks",
    "لپ‌لوبیایی",
    "M42 119 Q41 77 84 75 Q128 63 172 75 Q215 77 214 119 Q240 144 216 161 Q228 179 207 191 Q175 222 128 220 Q81 222 49 191 Q28 179 40 161 Q16 144 42 119Z",
  ),
  face(
    "Pixie",
    "پری‌کوچولو",
    "M43 119 Q39 78 85 75 Q128 62 171 75 Q217 78 213 119 L229 145 214 150 221 163 207 169 Q185 202 149 217 L128 227 107 217 Q71 202 49 169 L35 163 42 150 27 145Z",
  ),
  face(
    "Lion cub",
    "توله‌شیر",
    "M43 117 Q39 80 82 75 Q128 62 174 75 Q217 80 213 117 L228 128 220 144 231 155 217 169 222 183 202 187 197 202 179 203 169 218 148 215 128 226 108 215 87 218 77 203 59 202 54 187 34 183 39 169 25 155 36 144 28 128Z",
  ),
  face(
    "Rounded diamond",
    "لوزی نرم",
    "M43 119 Q39 82 82 77 Q128 57 174 77 Q217 82 213 119 L220 157 Q211 190 181 203 L128 226 75 203 Q45 190 36 157Z",
  ),
  face(
    "Chin fluff",
    "چونه‌پشمی",
    "M42 120 Q37 76 83 74 Q128 61 173 74 Q219 76 214 120 Q230 161 201 192 L178 209 157 212 146 223 136 218 128 231 120 218 110 223 99 212 78 209 55 192 Q26 161 42 120Z",
  ),
  face(
    "Cheek curls",
    "گونه‌فرفری",
    "M43 118 Q39 78 84 75 Q128 64 172 75 Q217 78 213 118 Q235 129 219 144 Q237 161 217 171 Q224 189 202 193 Q177 220 128 222 Q79 220 54 193 Q32 189 39 171 Q19 161 37 144 Q21 129 43 118Z",
    mirror(p("M39 151 q-6 9 4 11", "none", 1.6)),
  ),
  face(
    "Little bear",
    "خرسی",
    "M42 116 Q40 78 82 76 Q128 62 174 76 Q216 78 214 116 Q225 153 215 183 Q202 221 163 220 H93 Q54 221 41 183 Q31 153 42 116Z",
    mirror(p("M46 179 q3 12 12 18", "none", 1.4)),
  ),
  face(
    "Petal jaw",
    "چونه‌گلبرگی",
    "M42 118 Q40 77 87 75 Q128 63 169 75 Q216 77 214 118 Q229 162 201 185 Q201 204 180 207 Q168 226 147 217 Q128 231 109 217 Q88 226 76 207 Q55 204 55 185 Q27 162 42 118Z",
  ),
  face(
    "Comet tufts",
    "شهاب‌پشمی",
    "M43 118 Q39 76 85 74 Q128 62 171 74 Q217 76 213 118 L231 125 219 136 235 145 216 154 226 166 209 173 Q185 219 128 224 Q71 219 47 173 L30 166 40 154 21 145 37 136 25 125Z",
  ),
  face(
    "Round ruff",
    "یقه‌پشمی",
    "M43 118 Q39 77 85 74 Q128 62 171 74 Q217 77 213 118 Q228 157 210 178 L214 189 200 190 195 206 178 205 169 219 152 216 140 227 128 220 116 227 104 216 87 219 78 205 61 206 56 190 42 189 46 178 Q28 157 43 118Z",
  ),
  face(
    "Mooncake",
    "ماه‌کیک",
    "M42 118 Q37 77 83 74 Q128 60 173 74 Q219 77 214 118 Q224 167 203 192 Q183 216 154 217 L145 222 H111 L102 217 Q73 216 53 192 Q32 167 42 118Z",
    p("M119 215 h18", "none", 1.4),
  ),
  face(
    "Side sweep",
    "کاکل یک‌طرفه",
    "M43 120 Q38 84 78 77 Q80 64 96 66 L107 55 111 70 Q132 60 153 71 Q177 69 190 81 Q219 88 213 120 Q229 162 198 195 Q170 221 128 224 Q86 221 58 195 Q27 162 43 120Z",
  ),
  face(
    "Velvet",
    "مخملی",
    "M42 118 Q39 77 84 74 Q128 62 172 74 Q217 77 214 118 Q224 155 211 179 Q197 210 168 215 Q128 230 88 215 Q59 210 45 179 Q32 155 42 118Z",
    mirror(p("M44 163 l8 9 m-5 -20 6 7", "none", 1.4)),
  ),
  face(
    "Star cheeks",
    "گونه‌ستاره‌ای",
    "M43 119 Q38 78 86 74 Q128 62 170 74 Q218 78 213 119 L228 130 218 139 232 155 215 159 217 178 201 180 Q178 220 128 224 Q78 220 55 180 L39 178 41 159 24 155 38 139 28 130Z",
  ),
  face(
    "Milk bun",
    "نون‌شیری",
    "M42 120 Q36 78 86 75 Q128 64 170 75 Q220 78 214 120 Q226 155 213 180 Q211 211 181 214 Q158 228 128 220 Q98 228 75 214 Q45 211 43 180 Q30 155 42 120Z",
    p("M116 214 q12 4 24 0", "none", 1.2),
  ),
  face(
    "Teddy tufts",
    "خرسی پشمالو",
    "M43 119 Q39 77 85 74 Q128 62 171 74 Q217 77 213 119 L224 134 216 141 227 155 215 160 219 176 206 177 Q197 204 173 211 L155 217 147 212 128 225 109 212 101 217 83 211 Q59 204 50 177 L37 176 41 160 29 155 40 141 32 134Z",
  ),
  face(
    "Apricot",
    "زردآلو",
    "M42 119 Q38 78 84 75 Q128 62 172 75 Q218 78 214 119 Q225 164 199 193 Q171 224 128 219 Q85 224 57 193 Q31 164 42 119Z",
    p("M128 212 v6", "none", 1.4),
  ),
  face(
    "Snow tufts",
    "برفی پشمالو",
    "M43 118 Q40 78 86 75 L101 64 113 74 128 64 143 74 155 64 170 75 Q216 78 213 118 L225 139 215 149 226 166 209 173 Q187 216 148 220 L128 229 108 220 Q69 216 47 173 L30 166 41 149 31 139Z",
  ),
  face(
    "Cheek dimples",
    "لپ‌چال‌دار",
    "M43 118 Q39 77 84 74 Q128 62 172 74 Q217 77 213 118 Q227 139 217 157 Q225 184 201 198 Q177 220 128 222 Q79 220 55 198 Q31 184 39 157 Q29 139 43 118Z",
    mirror(p("M47 175 q-3 8 6 10", "none", 1.5)),
  ),
  face(
    "Tiny mane",
    "یال کوچولو",
    "M43 119 Q39 77 85 74 Q128 63 171 74 Q217 77 213 119 L228 139 217 146 228 161 212 166 215 183 198 184 193 202 176 202 163 218 144 216 128 228 112 216 93 218 80 202 63 202 58 184 41 183 44 166 28 161 39 146 28 139Z",
  ),
  face(
    "Button chin",
    "چونه‌دکمه‌ای",
    "M42 119 Q38 77 84 74 Q128 62 172 74 Q218 77 214 119 Q228 163 199 193 Q175 218 143 216 Q128 232 113 216 Q81 218 57 193 Q28 163 42 119Z",
    p("M122 217 q6 4 12 0", "none", 1.3),
  ),
  face(
    "Winged cheeks",
    "گونه‌بال‌دار",
    "M43 120 Q39 78 85 74 Q128 62 171 74 Q217 78 213 120 L233 136 217 144 234 157 213 162 221 176 202 180 Q177 219 128 223 Q79 219 54 180 L35 176 43 162 22 157 39 144 23 136Z",
  ),
  face(
    "Sleepy fluff",
    "پشم خواب‌آلود",
    "M43 119 Q39 79 85 75 L99 71 95 62 114 72 130 65 138 75 171 75 Q217 79 213 119 Q227 157 211 179 L214 191 198 192 Q177 218 147 220 L136 226 128 220 120 226 109 220 Q79 218 58 192 L42 191 45 179 Q29 157 43 119Z",
  ),
  face(
    "Pebble",
    "قلوه‌سنگی",
    "M42 118 Q38 78 84 74 Q128 62 172 74 Q218 78 214 118 L219 154 207 184 181 208 148 220 H108 L75 208 49 184 37 154Z",
  ),
  face(
    "Feather cheeks",
    "گونه‌پری",
    "M43 119 Q39 77 84 75 Q128 63 172 75 Q217 77 213 119 L225 131 216 139 228 148 216 154 224 163 211 168 214 179 201 182 Q178 219 128 224 Q78 219 55 182 L42 179 45 168 32 163 40 154 28 148 40 139 31 131Z",
  ),
  face(
    "Pudding",
    "پودینگ",
    "M42 119 Q38 77 84 75 Q128 63 172 75 Q218 77 214 119 Q224 154 214 180 Q208 207 180 216 Q153 222 128 218 Q103 222 76 216 Q48 207 42 180 Q32 154 42 119Z",
    mirror(p("M61 200 q9 7 19 9", "none", 1.3)),
  ),
  face(
    "Ruffled crown",
    "کاکل ژولیده",
    "M42 120 Q38 79 82 76 L94 63 105 73 112 59 126 72 139 58 147 72 162 63 174 76 Q218 79 214 120 Q228 163 200 193 Q171 221 128 224 Q85 221 56 193 Q28 163 42 120Z",
  ),
  face(
    "Dewdrop",
    "شبنم",
    "M43 119 Q39 78 84 75 Q128 62 172 75 Q217 78 213 119 Q229 162 200 190 Q175 210 128 230 Q81 210 56 190 Q27 162 43 119Z",
    p("M122 221 q6 4 12 0", "none", 1.3),
  ),
  face(
    "Round sideburns",
    "لپ پشمالو",
    "M43 119 Q39 77 84 75 Q128 63 172 75 Q217 77 213 119 Q229 123 226 135 Q239 143 227 153 Q236 167 218 173 Q220 188 203 192 Q178 218 128 223 Q78 218 53 192 Q36 188 38 173 Q20 167 29 153 Q17 143 30 135 Q27 123 43 119Z",
  ),
  face(
    "Tulip chin",
    "چونه‌لاله‌ای",
    "M42 119 Q38 77 84 74 Q128 62 172 74 Q218 77 214 119 Q228 163 199 191 Q180 211 161 211 Q149 228 128 219 Q107 228 95 211 Q76 211 57 191 Q28 163 42 119Z",
  ),
  face(
    "Ribbon fluff",
    "پشم روبانی",
    "M43 119 Q39 77 85 75 Q128 63 171 75 Q217 77 213 119 L226 138 215 147 226 165 209 174 207 189 190 193 Q166 222 128 224 Q90 222 66 193 L49 189 47 174 30 165 41 147 30 138Z",
    mirror(p("M43 156 l10 6 -6 9", "none", 1.3)),
  ),
  face(
    "Biscuit",
    "بیسکویتی",
    "M42 119 Q38 78 84 75 Q128 63 172 75 Q218 78 214 119 Q225 153 215 180 Q218 194 205 199 Q197 214 180 214 Q165 225 147 219 Q128 226 109 219 Q91 225 76 214 Q59 214 51 199 Q38 194 41 180 Q31 153 42 119Z",
  ),
  face(
    "Meadow fluff",
    "پشم بهاری",
    "M43 119 Q39 77 85 75 L100 67 111 75 128 66 145 75 156 67 171 75 Q217 77 213 119 L226 137 216 147 228 162 213 168 217 180 201 185 Q176 219 128 225 Q80 219 55 185 L39 180 43 168 28 162 40 147 30 137Z",
  ),
  face(
    "Lucky cat",
    "گربه خوش‌شانس",
    "M42 119 Q38 77 84 74 Q128 62 172 74 Q218 77 214 119 Q230 157 209 181 Q201 210 172 214 Q151 226 128 220 Q105 226 84 214 Q55 210 47 181 Q26 157 42 119Z",
    mirror(g(p("M43 155 l9 8 m-8 2 8 7", "none", 1.5), c(54, 183, 2, catInk))),
  ),
];

const ear = (
  name: string,
  fa: string,
  outline: string,
  inside?: ReactNode,
  other?: ReactNode,
) =>
  d(
    name,
    fa,
    g(
      p(outline, "currentColor", 3.8),
      inside,
      other || (
        <g transform="translate(256 0) scale(-1 1)">
          {g(p(outline, "currentColor", 3.8), inside)}
        </g>
      ),
    ),
  );
const inset = (outline: string) => p(outline, rose, 1.5);
export const earDesigns = [
  ear("Wishy points", "گوش‌های ویشی", "M43 121 Q30 73 48 34 Q69 42 91 70Z"),
  ear(
    "Soft pink",
    "صورتی مخملی",
    "M43 119 Q33 68 49 34 Q75 42 91 77Z",
    inset("M48 91 Q43 62 51 48 L76 78Z"),
  ),
  ear(
    "Folded tips",
    "نوک تاخورده",
    "M43 116 Q29 62 55 42 Q75 38 94 77 L74 71 58 57 56 93Z",
    p("M55 43 58 57 75 71", "none", 2),
  ),
  ear(
    "Lynx tassels",
    "منگوله سیاه‌گوش",
    "M44 116 41 48 46 30 52 44 56 28 62 49 91 79Z",
    inset("M49 93 49 59 71 80Z"),
  ),
  ear(
    "Round tips",
    "نوک گرد",
    "M42 116 Q24 50 48 40 Q66 33 91 79Z",
    inset("M48 92 Q37 60 48 55 Q58 52 74 81Z"),
  ),
  ear(
    "One flop",
    "یک گوش افتاده",
    "M43 118 Q26 58 51 39 Q71 37 91 79Z",
    inset("M49 93 47 54 76 79Z"),
    g(
      p(
        "M167 79 Q189 40 210 52 Q231 66 208 96 L196 78 204 65 Q188 72 185 100Z",
        "currentColor",
        3.8,
      ),
      p("M204 65 208 93", "none", 2),
    ),
  ),
  ear(
    "Petal ears",
    "گلبرگی",
    "M43 118 Q26 67 48 38 Q78 50 92 79Z",
    inset("M48 95 Q38 72 50 55 Q66 64 75 83Z"),
  ),
  ear(
    "Moon notch",
    "بریدگی هلالی",
    "M43 118 Q34 76 45 44 Q53 49 58 40 Q78 48 92 79Z",
    inset("M49 94 50 58 76 82Z"),
  ),
  ear(
    "Little curls",
    "گوش فرفری",
    "M43 118 Q28 69 48 43 Q62 29 73 45 Q74 60 62 57 Q56 52 62 47 L91 79Z",
    inset("M48 94 Q41 74 49 62 L74 82Z"),
  ),
  ear(
    "Leaf fold",
    "تاخورده برگی",
    "M43 117 Q32 58 59 39 Q80 51 91 80Z",
    g(inset("M49 95 58 54 77 82Z"), p("M58 54 58 83", "none", 1.5)),
  ),
  ear(
    "Cloud rim",
    "لبه ابری",
    "M43 118 Q33 92 37 71 Q29 62 39 55 Q35 41 48 39 Q57 30 65 43 Q82 54 92 80Z",
    inset("M48 96 Q41 66 51 52 L76 82Z"),
  ),
  ear(
    "Silver cuff",
    "حلقه نقره‌ای",
    "M43 119 Q32 68 49 35 Q72 43 92 79Z",
    g(
      inset("M49 94 50 52 76 81Z"),
      p("M36 76 52 72 54 81 37 85Z", "#d5dce8", 1.8),
    ),
  ),
  ear(
    "Twin tufts",
    "دو پره",
    "M43 117 38 63 44 37 53 45 62 33 66 55 92 79Z",
    inset("M49 95 49 58 77 82Z"),
  ),
  ear(
    "Ribbon tips",
    "نوک روبانی",
    "M43 118 Q32 70 48 36 Q67 39 92 79Z",
    g(
      inset("M48 94 50 54 75 81Z"),
      p("M47 45 39 35 52 37 61 29 61 45Z", lilac, 1.7),
    ),
  ),
  ear(
    "Tuft inside",
    "پشم توگوشی",
    "M43 118 Q32 70 49 35 Q73 44 92 79Z",
    g(
      inset("M48 94 50 52 77 82Z"),
      p("M46 88 53 76 57 87 64 78 66 91Z", white, 1.3),
    ),
  ),
  ear(
    "Star stud",
    "گوشواره ستاره",
    "M43 118 Q34 70 49 36 Q73 43 92 79Z",
    g(inset("M49 93 50 53 77 82Z"), star(43, 88)),
  ),
  ear(
    "Wide fan",
    "بادبزنی",
    "M42 117 Q19 69 44 40 Q74 44 93 80Z",
    g(
      inset("M45 94 Q31 65 46 54 L76 83Z"),
      p("M42 71 57 82 M45 63 63 78", "none", 1.3),
    ),
  ),
  ear(
    "Tucked pink",
    "گوش جمع‌شده",
    "M43 118 Q28 65 51 44 Q75 43 92 80Z",
    g(
      inset("M48 96 Q37 65 55 56 Q68 61 75 82Z"),
      p("M42 68 Q53 52 65 62", "none", 2),
    ),
  ),
  ear(
    "Freckled ears",
    "گوش خال‌دار",
    "M43 118 Q32 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 93 50 52 76 81Z"),
      c(54, 68, 2, catInk),
      c(60, 76, 2, catInk),
      c(53, 80, 1.7, catInk),
    ),
  ),
  ear(
    "Tiger tips",
    "نوک ببری",
    "M43 118 Q31 67 49 35 Q74 43 92 79Z",
    g(
      inset("M49 94 50 53 76 82Z"),
      p("M39 61 54 66 39 70Z M40 78 55 83 42 88Z", catInk, 0),
    ),
  ),
  ear(
    "Dew earrings",
    "گوشواره شبنم",
    "M43 118 Q33 69 49 35 Q73 43 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M37 92 Q29 105 37 108 Q45 105 37 92Z", mint, 1.6),
    ),
  ),
  ear(
    "Tiny hearts",
    "دل توگوشی",
    "M43 118 Q33 69 49 35 Q74 44 92 79Z",
    heart(56, 74),
  ),
  ear(
    "Left curl",
    "گوش پیچ‌خورده",
    "M43 118 Q28 62 48 39 Q60 31 66 43 Q72 56 60 59 L91 79Z",
    g(inset("M48 94 50 62 75 82Z"), p("M48 39 Q43 51 60 59", "none", 2)),
    g(
      p("M165 79 Q186 43 207 35 Q224 69 213 118Z", "currentColor", 3.8),
      p("M181 82 205 53 207 94Z", rose, 1.5),
    ),
  ),
  ear(
    "Both flops",
    "دو گوش افتاده",
    "M43 118 Q27 67 47 48 Q65 33 91 77 L66 72 49 89 47 66 Q43 80 49 98Z",
    p("M47 49 47 66 65 72", "none", 2),
  ),
  ear(
    "Soft fringe",
    "حاشیه پشمی",
    "M43 118 37 88 32 74 39 71 33 58 42 57 43 40 54 44 62 38 69 58 92 79Z",
    inset("M49 95 49 59 76 82Z"),
  ),
  ear(
    "Golden hoop",
    "حلقه طلایی",
    "M43 118 Q32 69 49 35 Q74 43 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      <ellipse
        cx="38"
        cy="94"
        rx="6"
        ry="8"
        fill="none"
        stroke={gold}
        strokeWidth="3"
      />,
    ),
  ),
  ear(
    "Shell fold",
    "صدفی",
    "M43 118 Q27 68 47 42 Q64 31 72 51 Q73 65 60 68 L92 79Z",
    g(
      inset("M49 96 Q40 78 48 65 L76 83Z"),
      p("M47 42 Q40 58 60 68 M48 52 Q47 60 57 61", "none", 1.7),
    ),
  ),
  ear(
    "Inner lightning",
    "برق توگوشی",
    "M43 118 Q33 68 49 35 Q73 44 92 79Z",
    p("M52 52 45 76 55 73 51 93 70 67 58 71 62 58Z", gold, 0),
  ),
  ear(
    "Rounded fold",
    "تاخورده گرد",
    "M43 118 Q29 69 44 48 Q57 32 72 49 Q82 57 72 67 L92 80Z",
    g(inset("M49 95 49 65 76 82Z"), p("M44 48 Q47 66 72 67", "none", 2)),
  ),
  ear(
    "Pearl trio",
    "سه مروارید",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 82Z"),
      c(38, 80, 3, white),
      c(38, 88, 3, white),
      c(40, 96, 3, white),
    ),
  ),
  ear(
    "Leaf tip",
    "برگ روی گوش",
    "M43 118 Q33 69 49 35 Q73 44 92 79Z",
    g(inset("M49 94 50 53 76 81Z"), leaf(48, 45)),
  ),
  ear(
    "Notched fluff",
    "پشمی شکاف‌دار",
    "M43 118 37 79 42 59 38 51 47 52 51 35 63 44 67 60 92 79Z",
    g(inset("M49 94 51 58 76 81Z"), p("M39 82 47 86 42 94", "none", 1.7)),
  ),
  ear(
    "Sewn patch",
    "وصله توگوشی",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M49 70 62 68 69 83 53 87Z", lilac, 1.4),
      p("M49 74 54 74 M52 82 56 81 M61 70 61 74", "none", 1.2),
    ),
  ),
  ear(
    "Sunrise",
    "طلوع توگوشی",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M48 87 Q59 69 71 87Z", gold, 0),
      p("M59 70 v-6 m-9 10 -4 -4 m22 5 3 -5", "none", 1.4),
    ),
  ),
  ear(
    "Feather tufts",
    "پره‌ای",
    "M43 118 35 88 39 68 35 60 44 59 41 47 51 50 54 35 65 54 92 79Z",
    g(inset("M49 94 51 60 76 82Z"), p("M46 91 53 80 58 89", white, 1.4)),
  ),
  ear(
    "Flower stud",
    "گوشواره گل",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(inset("M49 94 50 53 76 81Z"), c(38, 88, 6, rose), c(38, 88, 2.5, gold)),
  ),
  ear(
    "High fold",
    "تای بالایی",
    "M43 118 Q32 70 48 35 L64 42 69 59 92 79Z",
    g(inset("M49 94 51 58 76 82Z"), p("M48 35 50 56 69 59", rose, 2)),
  ),
  ear(
    "Little waves",
    "گوش موجی",
    "M43 118 Q31 74 40 55 Q35 40 49 36 Q61 35 63 48 Q78 56 92 79Z",
    g(
      inset("M49 94 Q42 75 51 57 L76 82Z"),
      p("M47 70 q8 -6 13 3 m-13 7 q8 -6 13 3", "none", 1.4),
    ),
  ),
  ear(
    "Crescent stud",
    "گوشواره ماه",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M37 83 Q25 94 38 103 Q31 92 43 88Z", gold, 1.3),
    ),
  ),
  ear(
    "Inner bow",
    "پاپیون توگوشی",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M58 78 49 70 47 83 58 78 67 68 70 81Z", lilac, 1.3),
      c(58, 78, 2.5, gold),
    ),
  ),
  ear(
    "Heart notch",
    "شکاف قلبی",
    "M43 118 Q33 69 48 36 L53 43 59 38 Q78 51 92 79Z",
    inset("M49 94 51 58 76 82Z"),
  ),
  ear(
    "Panda tips",
    "نوک پاندایی",
    "M43 118 Q28 68 48 35 Q74 43 92 79Z",
    g(
      p("M35 64 Q38 44 48 35 Q65 42 74 54 L54 58Z", catInk, 0),
      inset("M49 94 51 63 76 82Z"),
    ),
  ),
  ear(
    "Two cuffs",
    "دو حلقه گوش",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M36 75 49 72 51 78 37 82Z", mint, 1.5),
      p("M37 85 51 82 52 88 38 92Z", gold, 1.5),
    ),
  ),
  ear(
    "Open curl",
    "پیچ باز",
    "M43 118 Q27 63 48 40 Q69 32 72 53 Q70 66 59 62 L91 79Z",
    g(inset("M49 94 49 66 76 82Z"), p("M48 40 Q39 58 59 62", "none", 1.7)),
  ),
  ear(
    "Candy stripe",
    "راه‌راه آبنباتی",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M50 64 59 63 M50 76 68 73 M50 87 73 81", "none", 2),
    ),
  ),
  ear(
    "Petal stud",
    "گلبرگ آویز",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p("M38 88 Q24 96 36 107 Q47 100 38 88Z", rose, 1.5),
      p("M38 91 36 103", "none", 1.2),
    ),
  ),
  ear(
    "Side tufts",
    "پشم کنار گوش",
    "M43 118 35 90 30 81 38 79 34 65 41 65 Q39 47 49 35 Q74 44 92 79Z",
    inset("M49 94 50 53 76 81Z"),
  ),
  ear(
    "Comet earring",
    "گوشواره شهاب",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      star(37, 93),
      p("M38 81 30 75 M42 79 38 71", "none", 1.8),
    ),
  ),
  ear(
    "Butterfly bow",
    "پروانه توگوشی",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      p(
        "M58 78 Q43 60 46 79 Q44 91 58 80 Q75 86 68 75 Q67 62 58 78Z",
        mint,
        1.4,
      ),
      p("M58 75 59 83", "none", 2),
    ),
  ),
  ear(
    "Wish sparkle",
    "برق آرزو",
    "M43 118 Q33 68 49 35 Q74 44 92 79Z",
    g(
      inset("M49 94 50 53 76 81Z"),
      star(56, 72, white),
      c(48, 88, 2, gold),
      c(64, 84, 1.5, gold),
    ),
  ),
];

export type EyeDesign = {
  name: string;
  fa: string;
  left: string;
  right?: string;
  detail?: ReactNode;
};
const eye = (
  name: string,
  fa: string,
  left: string,
  detail?: ReactNode,
  right?: string,
): EyeDesign => ({ name, fa, left, right, detail });
// Local eye coordinates: left at (51,110), right reflected around x=128.
// Every aperture remains large, including sleepy expressions. No closed slits.
export const eyeDesigns = [
  eye("Wishy gaze", "نگاه ویشی", "M1 8 67 32 V43 C67 88 3 88 3 43Z"),
  eye(
    "Moon round",
    "گرد مثل ماه",
    "M1 32 C1 -8 67 -8 67 32 V43 C67 87 1 87 1 43Z",
  ),
  eye(
    "Curious almond",
    "بادامی کنجکاو",
    "M0 27 Q32 -3 68 24 L66 48 Q58 80 30 75 Q1 73 0 44Z",
  ),
  eye(
    "Soft sleepy",
    "خواب‌آلود نرم",
    "M0 22 Q34 34 68 22 V44 C68 87 1 87 1 44Z",
    mirror(p("M58 123 Q83 130 109 125", "none", 1.5)),
  ),
  eye(
    "Bright teardrop",
    "اشکی براق",
    "M1 27 Q8 1 34 0 Q66 9 68 42 Q68 78 35 77 Q0 74 1 27Z",
  ),
  eye(
    "Swooping wings",
    "نگاه بال‌دار",
    "M0 13 Q22 25 67 20 Q73 61 49 73 Q9 89 3 49Z",
    mirror(p("M51 123 45 115 M54 130 47 127", "none", 2)),
  ),
  eye(
    "Gentle arch",
    "قوس مهربون",
    "M0 25 Q34 -11 68 25 V44 Q65 78 34 77 Q3 78 0 44Z",
  ),
  eye(
    "Pillow eyes",
    "چشم بالشتی",
    "M1 17 Q2 8 16 8 H53 Q67 8 67 22 V55 Q64 78 35 77 Q3 78 1 55Z",
  ),
  eye(
    "Cheeky wink",
    "شیطونک",
    "M1 17 Q33 4 67 18 V46 Q64 79 32 76 Q0 74 1 44Z",
    undefined,
    "M1 29 Q35 38 67 19 V44 Q67 79 34 76 Q1 76 1 44Z",
  ),
  eye(
    "Velvet cat eye",
    "مخملی کشیده",
    "M0 7 Q19 21 67 24 L65 51 Q57 79 30 75 Q1 73 2 44Z",
    mirror(p("M51 118 47 111", "none", 2.5)),
  ),
  eye(
    "Dewy",
    "نم‌نم",
    "M1 31 Q2 1 32 2 Q63 -2 67 30 L65 51 Q57 78 31 77 Q0 76 1 45Z",
    mirror(c(62, 173, 2.5, rose)),
  ),
  eye(
    "Questioning",
    "پرسشگر",
    "M0 22 Q25 -2 66 21 V46 Q64 79 33 76 Q1 75 0 44Z",
    undefined,
    "M0 8 Q36 4 67 25 V45 Q63 80 32 76 Q0 73 0 43Z",
  ),
  eye(
    "Lower lashes",
    "مژه پایینی",
    "M1 21 Q31 0 67 21 V45 Q66 78 34 77 Q2 77 1 45Z",
    mirror(p("M65 178 62 183 M72 182 71 187", "none", 1.7)),
  ),
  eye(
    "Upturned",
    "گوشه خندون",
    "M0 16 Q28 31 68 7 L66 45 Q64 80 31 76 Q0 75 0 43Z",
  ),
  eye(
    "Dreamy hood",
    "پلک رویایی",
    "M1 15 Q34 31 67 15 L66 48 Q62 80 32 76 Q2 76 1 45Z",
    mirror(p("M54 119 Q83 134 115 119", "none", 1.7)),
  ),
  eye(
    "Lotus",
    "نیلوفری",
    "M0 24 Q20 1 37 5 Q56 6 68 23 L66 50 Q59 80 32 77 Q2 75 0 44Z",
    mirror(p("M53 126 48 121 M56 121 53 115", "none", 1.8)),
  ),
  eye(
    "Big wonder",
    "تعجب شیرین",
    "M1 29 C1 -4 65 -6 67 29 L66 49 C63 84 3 84 1 49Z",
    mirror(p("M60 112 Q82 102 105 112", "none", 1.5)),
  ),
  eye(
    "Little fox",
    "روباه کوچولو",
    "M0 12 67 26 Q75 62 49 75 Q8 88 3 46Z",
    mirror(p("M52 123 45 118 48 128", catInk, 0)),
  ),
  eye(
    "Droopy sweet",
    "افتاده مهربون",
    "M0 22 Q32 5 67 14 V45 Q66 79 34 77 Q1 76 0 46Z",
  ),
  eye(
    "Round lashes",
    "گرد مژه‌دار",
    "M1 29 C1 -5 67 -5 67 29 V45 C67 83 1 83 1 45Z",
    mirror(p("M58 120 53 113 M64 114 61 107", "none", 2)),
  ),
  eye(
    "Mischief",
    "شیطنت",
    "M0 16 Q27 13 67 36 V48 Q61 79 31 76 Q1 75 0 43Z",
    undefined,
    "M0 7 Q38 18 67 31 V48 Q61 79 31 76 Q1 75 0 43Z",
  ),
  eye(
    "Cloud corners",
    "گوشه ابری",
    "M1 24 Q1 8 16 10 Q34 -3 52 10 Q67 7 67 24 V45 Q68 78 34 77 Q0 78 1 45Z",
  ),
  eye(
    "Tucked lids",
    "پلک جمع‌شده",
    "M0 18 Q34 11 68 18 L65 48 Q60 79 32 76 Q4 78 2 47Z",
    mirror(p("M60 122 Q85 117 110 123", "none", 1.7)),
  ),
  eye(
    "Petal lashes",
    "مژه گلبرگی",
    "M0 25 Q32 -2 68 25 L66 48 Q61 78 33 77 Q1 76 0 45Z",
    mirror(p("M53 129 Q44 126 48 121 Q52 119 56 126", catInk, 0)),
  ),
  eye(
    "Lazy Sunday",
    "جمعه خوابالو",
    "M0 24 68 29 V47 Q66 80 33 77 Q0 78 0 44Z",
    mirror(p("M57 126 111 131", "none", 1.4)),
  ),
  eye(
    "Diamond round",
    "لوزی گرد",
    "M0 27 20 7 Q34 0 48 7 L68 27 V45 Q63 78 34 77 Q5 78 0 45Z",
  ),
  eye(
    "Tilted curious",
    "کنجکاو کجکی",
    "M0 30 Q26 1 67 17 V45 Q64 78 34 77 Q0 77 0 46Z",
    undefined,
    "M0 17 Q41 1 67 30 V46 Q67 77 33 77 Q3 78 0 45Z",
  ),
  eye(
    "Silky lashes",
    "مژه ابریشمی",
    "M0 18 Q33 2 68 19 L65 47 Q61 79 33 77 Q0 77 1 44Z",
    mirror(p("M52 127 45 122 M55 121 48 115 M61 117 56 110", "none", 1.7)),
  ),
  eye(
    "Butterfly corners",
    "گوشه پروانه‌ای",
    "M0 17 Q11 5 19 15 Q40 2 68 21 L66 47 Q63 78 33 77 Q0 76 0 44Z",
    mirror(p("M51 127 Q41 117 47 114 Q54 112 57 121", catInk, 0)),
  ),
  eye(
    "Soft trapezoid",
    "ذوزنقه نرم",
    "M0 13 Q35 14 68 26 L64 54 Q58 79 32 76 Q4 77 2 47Z",
  ),
  eye(
    "Crescent rim",
    "حاشیه هلالی",
    "M0 20 Q35 0 68 20 L66 47 Q60 77 34 77 Q3 78 0 45Z",
    mirror(p("M61 176 Q84 190 107 176", "none", 1.4)),
  ),
  eye(
    "Baby owl",
    "جغد کوچولو",
    "M0 28 Q0 5 25 5 L34 0 43 5 Q68 5 68 28 V46 Q68 81 34 78 Q0 81 0 46Z",
  ),
  eye(
    "Warm smile",
    "لبخند نگاه",
    "M0 25 Q33 -3 68 25 L65 47 Q58 68 34 69 Q9 68 3 47Z",
    mirror(p("M56 180 Q83 192 111 180", "none", 1.5)),
  ),
  eye(
    "Folded silk",
    "پلک ابریشمی",
    "M0 12 Q32 24 68 18 V46 Q66 80 34 77 Q1 77 0 45Z",
    mirror(p("M55 116 Q83 127 114 122", "none", 1.7)),
  ),
  eye(
    "Spark corner",
    "چشم جرقه‌ای",
    "M0 26 Q32 -3 68 22 V46 Q67 80 34 77 Q0 78 0 45Z",
    mirror(star(49, 120, catInk)),
  ),
  eye(
    "Tender slope",
    "شیب مهربون",
    "M0 27 Q28 13 68 7 V44 Q65 80 34 77 Q1 76 0 45Z",
    mirror(p("M54 129 47 125", "none", 2)),
  ),
  eye(
    "Oval hood",
    "بیضی پلک‌دار",
    "M0 27 Q3 6 34 8 Q65 7 68 27 L65 48 Q60 80 34 77 Q6 80 2 48Z",
    mirror(p("M59 115 Q83 104 109 116", "none", 1.5)),
  ),
  eye(
    "Long wing",
    "بال بلند",
    "M0 6 Q29 19 68 25 V47 Q64 79 34 77 Q3 76 2 44Z",
    mirror(p("M51 116 Q44 116 42 107 L58 120Z", catInk, 0)),
  ),
  eye(
    "Soft octagon",
    "هشت‌گوش نرم",
    "M0 25 13 9 Q34 -2 55 9 L68 25 66 51 53 70 Q34 82 15 70 L2 51Z",
  ),
  eye(
    "Morning gaze",
    "نگاه صبحگاهی",
    "M0 20 Q31 9 68 14 V47 Q64 79 34 77 Q1 77 0 45Z",
    mirror(p("M58 116 Q81 109 109 115 M57 181 l-3 4", "none", 1.5)),
  ),
  eye(
    "Shy lashes",
    "مژه خجالتی",
    "M0 29 Q34 3 68 16 L65 47 Q61 79 34 77 Q1 76 0 45Z",
    mirror(p("M53 134 46 130 M56 126 50 121", "none", 2)),
  ),
  eye(
    "Bubble round",
    "گرد حبابی",
    "M0 28 Q0 6 21 5 Q34 -5 47 5 Q68 6 68 28 V46 Q69 81 34 78 Q-1 81 0 46Z",
    mirror(c(54, 169, 2.5, white)),
  ),
  eye(
    "Swan sweep",
    "قوس قو",
    "M0 10 Q21 4 29 17 Q45 31 68 22 V46 Q67 80 34 77 Q1 77 0 44Z",
    mirror(p("M51 120 Q44 119 44 113", "none", 2)),
  ),
  eye(
    "Cheek dimples",
    "نگاه چال‌دار",
    "M0 24 Q32 -3 68 23 L66 49 Q62 78 34 77 Q3 78 0 46Z",
    mirror(g(p("M55 177 q-6 4 -3 9", "none", 1.7), c(58, 190, 1.6, catInk))),
  ),
  eye(
    "Playful arch",
    "قوس بازیگوش",
    "M0 21 Q26 -2 68 20 V46 Q67 80 34 77 Q0 78 0 45Z",
    undefined,
    "M0 14 Q42 -2 68 26 V46 Q68 78 34 77 Q1 80 0 46Z",
  ),
  eye(
    "Two petal lashes",
    "دو مژه گلبرگی",
    "M0 24 Q33 0 68 21 V46 Q65 80 34 77 Q1 76 0 45Z",
    mirror(
      p(
        "M52 131 Q42 123 48 120 Q53 118 56 126 M56 122 Q47 113 54 111 Q59 111 61 118",
        catInk,
        0,
      ),
    ),
  ),
  eye(
    "Honey drop",
    "قطره عسل",
    "M0 28 Q5 5 28 2 Q53 -3 68 25 L66 47 Q64 77 34 78 Q1 79 0 45Z",
    mirror(p("M56 172 Q59 182 67 183", "none", 1.6)),
  ),
  eye(
    "Softly squared",
    "چهارگوش مهربون",
    "M0 21 Q0 10 13 10 L55 16 Q68 17 68 30 V50 Q65 79 34 77 Q1 79 0 50Z",
  ),
  eye(
    "Ribbon corners",
    "گوشه روبانی",
    "M0 19 Q31 2 68 22 V46 Q66 80 34 77 Q1 77 0 45Z",
    mirror(p("M52 129 44 120 42 131 52 129 47 139Z", catInk, 0)),
  ),
  eye(
    "Stargazer",
    "ستاره‌بین",
    "M0 28 Q2 1 34 1 Q66 1 68 28 L66 47 Q62 81 34 78 Q6 81 2 47Z",
    mirror(g(star(51, 118, catInk), c(61, 109, 1.7, catInk))),
  ),
];
export function EyeShapes({
  value,
  outlineOnly = false,
}: {
  value: number;
  outlineOnly?: boolean;
}) {
  const style = eyeDesigns[value] || eyeDesigns[0];
  return (
    <g data-eye-apertures="large">
      <path
        transform="translate(51 110)"
        d={style.left}
        fill={outlineOnly ? "none" : white}
        {...line}
        strokeWidth="3.5"
      />
      <path
        transform="translate(205 110) scale(-1 1)"
        d={style.right || style.left}
        fill={outlineOnly ? "none" : white}
        {...line}
        strokeWidth="3.5"
      />
      {outlineOnly && style.detail}
    </g>
  );
}
export function EyeMask({ value }: { value: number }) {
  const style = eyeDesigns[value] || eyeDesigns[0];
  return (
    <>
      <path transform="translate(51 110)" d={style.left} />
      <path
        transform="translate(205 110) scale(-1 1)"
        d={style.right || style.left}
      />
    </>
  );
}
// The black field stays broad. Distinction comes from gaze, pupil silhouette and
// individually drawn reflections, rather than reducing the pupil to a small dot.
const shine = (outline: string, width = 2) => (
  <path
    d={outline}
    fill="none"
    stroke={white}
    strokeWidth={width}
    strokeLinecap="round"
  />
);
const pupil = (
  name: string,
  fa: string,
  reflection?: ReactNode,
  gazeX = 0,
  gazeY = 0,
  shape?: string,
) =>
  d(
    name,
    fa,
    g(
      ...[85, 171].map((x, i) => (
        <g transform={`translate(${x + gazeX} ${141 + gazeY})`}>
          {shape ? p(shape, catInk, 0) : e(0, 0, 26, 33, catInk)}
          <g transform={`translate(0 10) scale(${i ? -1 : 1} 1)`}>
            {reflection}
          </g>
        </g>
      )),
    ),
  );
export const pupilDesigns = [
  pupil("Logo black", "سیاهی لوگو"),
  pupil("Double gloss", "برق دوتایی", g(e(-10, -12, 6, 8), c(10, 13, 3))),
  pupil(
    "Window light",
    "نور پنجره",
    g(
      p("M-17 -19 h12 v13 h-12Z", white, 0),
      p("M-2 -19 h6 v13 h-6Z", white, 0),
      c(12, 16, 2.5),
    ),
  ),
  pupil(
    "Crescent glow",
    "برق هلالی",
    p("M-15 -23 Q-28 -5 -13 9 Q-22 -5 -7 -20Z", white, 0),
  ),
  pupil("Tiny heart", "دل توچشمی", g(heart(-8, -10, white), c(12, 13, 3))),
  pupil("North star", "ستاره قطبی", g(star(-10, -13, white), c(11, 13, 3))),
  pupil("Looking left", "نگاه به چپ", g(e(-8, -14, 4, 7), c(10, 13, 2.5)), -5),
  pupil(
    "Looking right",
    "نگاه به راست",
    g(e(-8, -14, 4, 7), c(10, 13, 2.5)),
    5,
  ),
  pupil(
    "Cloud reflection",
    "بازتاب ابر",
    g(
      p(
        "M-18 -10 Q-23 -19 -15 -20 Q-9 -30 -3 -20 Q8 -23 9 -13 Q6 -8 -1 -10Z",
        white,
        0,
      ),
      c(12, 15, 3),
    ),
  ),
  pupil(
    "Cat slit",
    "مردمک گربه‌ای",
    g(p("M0 -22 Q-7 0 0 24 Q7 0 0 -22Z", gold, 0), e(-13, -12, 4, 7)),
  ),
  pupil(
    "Star trail",
    "رد ستاره",
    g(star(-10, -14, white), c(3, 0, 2.4), c(13, 12, 1.8)),
  ),
  pupil(
    "Butterfly light",
    "نور پروانه",
    p(
      "M-5 -12 Q-21 -27 -21 -11 Q-20 -3 -6 -9 Q-1 4 6 -4 Q10 -19 -5 -12Z",
      white,
      0,
    ),
  ),
  pupil(
    "Diamond light",
    "برق الماسی",
    g(p("M-10 -23 -2 -13 -10 -3 -18 -13Z", white, 0), c(12, 13, 3)),
  ),
  pupil(
    "Moon and star",
    "ماه و ستاره",
    g(
      p("M-10 -23 Q-25 -14 -12 -3 Q-17 -15 -4 -17Z", white, 0),
      star(11, 13, white),
    ),
  ),
  pupil(
    "Paw reflection",
    "رد پنجه",
    g(
      e(-8, -8, 6, 5),
      c(-16, -16, 2.8),
      c(-9, -20, 2.8),
      c(-2, -16, 2.8),
      c(13, 14, 2.5),
    ),
  ),
  pupil(
    "Sunbeam",
    "پرتو خورشید",
    g(
      c(-9, -12, 6),
      shine("M-9 -24 v4 m-12 8 h4 m8 12 v-4 m12 -8 h-4", 1.5),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Upward wonder",
    "نگاه رو به بالا",
    g(e(-9, -12, 5, 7), c(12, 9, 2.5)),
    0,
    -5,
  ),
  pupil(
    "Shy downward",
    "نگاه خجالتی",
    g(e(-10, -15, 5, 6), c(12, 9, 2.5)),
    0,
    4,
  ),
  pupil(
    "Honey rings",
    "حلقه عسلی",
    g(
      <ellipse
        cx="0"
        cy="1"
        rx="18"
        ry="26"
        fill="none"
        stroke={gold}
        strokeWidth="3"
      />,
      e(-9, -14, 5, 7),
    ),
  ),
  pupil(
    "Violet rings",
    "حلقه بنفش",
    g(
      <ellipse
        cx="0"
        cy="1"
        rx="18"
        ry="26"
        fill="none"
        stroke={lilac}
        strokeWidth="3"
      />,
      star(-10, -13, white),
    ),
  ),
  pupil(
    "Leaf reflection",
    "بازتاب برگ",
    g(
      p("M-17 -5 Q-24 -25 -4 -21 Q3 -6 -17 -5Z", white, 0),
      p("M-17 -6 -6 -18", "none", 1.4),
      c(12, 15, 3),
    ),
  ),
  pupil(
    "Ribbon reflection",
    "بازتاب روبان",
    g(p("M-8 -12 -21 -23 -22 -5 -8 -12 5 -23 6 -5Z", white, 0), c(12, 14, 3)),
  ),
  pupil(
    "Comet",
    "شهاب",
    g(
      p("M-18 -21 -7 -15 -15 -5Z", white, 0),
      star(-5, -6, white),
      c(12, 16, 2.5),
    ),
  ),
  pupil(
    "Three glints",
    "سه برق ریز",
    g(e(-12, -14, 4, 7), c(2, -19, 3), c(13, 15, 3)),
  ),
  pupil(
    "Jellybean gloss",
    "برق پاستیلی",
    g(
      p("M-17 -19 Q-8 -27 -3 -17 Q-5 -7 -13 -8 Q-21 -11 -17 -19Z", white, 0),
      c(12, 14, 3),
    ),
  ),
  pupil(
    "Twin hearts",
    "دوتا دل",
    g(
      heart(-9, -12, white),
      <g transform="translate(13 12) scale(.5)">{heart(0, 0, white)}</g>,
    ),
  ),
  pupil(
    "Flower light",
    "نور گل",
    g(
      c(-10, -16, 4),
      c(-15, -11, 4),
      c(-5, -11, 4),
      c(-10, -6, 4),
      c(-10, -11, 2, catInk),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Round square",
    "مردمک کوسنی",
    g(e(-12, -13, 4, 7), c(12, 14, 3)),
    0,
    0,
    "M-24 -19 Q-24 -32 -10 -32 H10 Q24 -32 24 -19 V16 Q24 34 0 34 Q-24 34 -24 16Z",
  ),
  pupil(
    "Dream drops",
    "قطره‌های رویا",
    g(
      p("M-12 -24 Q-24 -10 -12 -7 Q0 -10 -12 -24Z", white, 0),
      p("M10 7 Q3 15 10 17 Q17 15 10 7Z", white, 0),
    ),
  ),
  pupil(
    "Spark cluster",
    "خوشه جرقه",
    g(star(-13, -11, white), star(1, -20, white), c(13, 13, 2.5)),
  ),
  pupil(
    "Milky swirl",
    "پیچ شیری",
    g(
      shine("M-18 -15 Q-5 -31 4 -15 Q6 -5 -3 -4 Q-11 -6 -5 -13", 3),
      c(14, 15, 2.5),
    ),
  ),
  pupil(
    "Half-moon gloss",
    "برق نیم‌ماه",
    g(
      p("M-19 -21 Q-3 -26 -2 -12 Q-3 -4 -14 -6 Q-5 -12 -19 -21Z", white, 0),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Soft diamond pupil",
    "مردمک لوزی نرم",
    g(e(-11, -11, 5, 7), c(11, 15, 3)),
    0,
    0,
    "M0 -36 Q14 -29 26 -4 Q30 17 0 36 Q-30 17 -26 -4 Q-14 -29 0 -36Z",
  ),
  pupil(
    "Firefly",
    "کرم شب‌تاب",
    g(e(-10, -11, 5, 9, gold), c(-11, -14, 3), c(12, 13, 2.5)),
  ),
  pupil(
    "Snow sparkle",
    "برق برفی",
    g(shine("M-10 -23 v20 m-9 -15 18 10 m-18 0 18 -10", 2), c(12, 13, 3)),
  ),
  pupil(
    "Two windows",
    "دو پنجره",
    g(
      p(
        "M-18 -22 h10 v10 h-10Z M-5 -22 h10 v10 h-10Z M-18 -9 h10 v7 h-10Z M-5 -9 h10 v7 h-10Z",
        white,
        0,
      ),
      c(13, 15, 2.5),
    ),
  ),
  pupil(
    "Ocean glimmer",
    "برق دریایی",
    g(
      p(
        "M-21 -11 Q-14 -23 -7 -13 Q-2 -23 5 -13 L3 -7 Q-4 -17 -9 -7 Q-14 -17 -19 -5Z",
        mint,
        0,
      ),
      c(12, 14, 3),
    ),
  ),
  pupil(
    "Little planet",
    "سیاره کوچولو",
    g(
      c(-9, -12, 6),
      <ellipse
        cx="-9"
        cy="-12"
        rx="11"
        ry="3"
        transform="rotate(-25 -9 -12)"
        fill="none"
        stroke={white}
        strokeWidth="1.5"
      />,
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Heart pupil",
    "مردمک قلبی",
    g(e(-12, -11, 4, 6), c(12, 12, 3)),
    0,
    0,
    "M0 31 C-46 5 -29 -40 0 -22 C29 -40 46 5 0 31Z",
  ),
  pupil(
    "Rainbow arc",
    "کمان رنگین",
    g(
      shine("M-20 -8 Q-10 -28 3 -11", 4),
      p("M-16 -6 Q-9 -19 -1 -8", lilac, 0),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Confetti",
    "کاغذرنگی",
    g(
      p("M-17 -20 h6 v9 h-6Z M-4 -18 l5 -3 4 8 -5 3Z", white, 0),
      c(-10, -4, 2.8),
      p("M10 10 16 13 12 18 7 14Z", white, 0),
    ),
  ),
  pupil(
    "Book light",
    "نور کتاب",
    g(
      p(
        "M-9 -17 Q-16 -23 -22 -20 V-7 Q-16 -10 -9 -5 Q-2 -10 4 -7 V-20 Q-2 -23 -9 -17Z",
        white,
        0,
      ),
      p("M-9 -16 v10", "none", 1.2),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Golden diamond",
    "الماس طلایی",
    g(
      p("M-10 -24 -3 -13 -10 -3 -17 -13Z", gold, 0),
      c(-11, -15, 2, white),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Ribbon gleam",
    "برق نواری",
    g(
      p("M-20 -17 Q-10 -27 2 -16 L-1 -10 Q-11 -18 -17 -10Z", white, 0),
      p("M8 8 15 14 11 18 5 12Z", white, 0),
    ),
  ),
  pupil(
    "Tiny flame",
    "شعله کوچولو",
    g(
      p(
        "M-10 -25 Q-18 -17 -13 -13 Q-23 -12 -16 -3 Q-3 2 -2 -10 Q-2 -18 -10 -25Z",
        gold,
        0,
      ),
      e(-11, -8, 2.5, 4),
      c(13, 15, 3),
    ),
  ),
  pupil(
    "Polka light",
    "نور خال‌خالی",
    g(c(-14, -17, 4), c(-3, -18, 3), c(-10, -7, 3), c(13, 14, 3)),
  ),
  pupil(
    "Wing reflection",
    "بازتاب بال",
    g(
      p(
        "M-16 -5 Q-25 -23 -6 -24 L-9 -16 2 -20 -3 -11 4 -12 Q-1 -3 -16 -5Z",
        white,
        0,
      ),
      c(12, 14, 3),
    ),
  ),
  pupil(
    "Little wish",
    "آرزوی کوچولو",
    g(
      star(-9, -13, gold),
      c(-10, -14, 2),
      shine("M4 -24 l4 -4 m0 11 5 -1", 1.5),
      c(13, 14, 3),
    ),
  ),
  pupil(
    "Mint slit",
    "مردمک نعنایی",
    g(
      p("M0 -25 Q-10 -1 0 25 Q10 -1 0 -25Z", mint, 0),
      e(-13, -12, 4, 7),
      c(13, 15, 2.5),
    ),
  ),
  pupil(
    "Stardust",
    "غبار ستاره",
    g(
      star(-11, -13, white),
      c(1, -23, 2),
      c(10, -10, 1.8),
      c(6, 7, 2),
      star(14, 18, white),
    ),
  ),
];

const brow = (
  name: string,
  fa: string,
  outline: string,
  detail?: ReactNode,
  fill = "none",
) => d(name, fa, mirror(g(p(outline, fill, 2.4), detail)));
export const browDesigns = [
  d("Natural forehead", "پیشونی ساده", null),
  brow("Gentle arches", "قوس آروم", "M67 105 Q84 94 101 104"),
  brow("Curious lift", "ابروی کنجکاو", "M66 100 Q82 86 99 100"),
  brow("Soft dashes", "خط نرم", "M70 102 96 102"),
  brow("Little tufts", "پشم ابرویی", "M69 105 75 97 80 103 86 95 94 103"),
  brow("Silk sweep", "قوس ابریشمی", "M65 104 Q78 94 100 98"),
  brow("Sleepy waves", "موج خوابالو", "M66 104 Q77 99 84 104 T102 102"),
  brow(
    "Double arch",
    "قوس دوتایی",
    "M68 105 Q83 95 99 104 M73 97 Q84 91 94 96",
  ),
  brow("Kitten ticks", "خط‌های بچه‌گربه", "M73 103 78 98 M86 98 92 103"),
  brow("Round commas", "ابروی ویرگولی", "M69 104 Q74 94 82 98 Q88 105 96 101"),
  brow(
    "Willow brows",
    "ابروی بیدی",
    "M66 105 Q78 90 101 100 Q84 97 66 105Z",
    undefined,
    catInk,
  ),
  brow("Friendly slope", "شیب مهربون", "M68 98 100 105"),
  brow("Upward slope", "شیب رو به بالا", "M68 105 100 96"),
  brow(
    "Dotted arches",
    "قوس نقطه‌ای",
    "M72 102 Q84 95 96 102",
    g(c(66, 106, 1.6, catInk), c(102, 106, 1.6, catInk)),
  ),
  brow(
    "Moon commas",
    "ویرگول ماهی",
    "M69 104 Q73 93 85 97 Q75 97 76 105Z",
    undefined,
    catInk,
  ),
  brow(
    "Feather brow",
    "ابروی پری",
    "M67 105 Q81 92 100 103 M75 100 73 94 M82 97 82 91 M90 98 94 93",
  ),
  brow("Split sweep", "قوس دو تکه", "M66 104 78 98 M86 97 101 101"),
  brow(
    "Three fur strokes",
    "سه تار پشم",
    "M72 104 77 97 M82 102 86 94 M92 103 96 98",
  ),
  brow("Wavy ribbon", "روبان موجی", "M65 103 Q75 93 84 101 Q94 108 102 98"),
  brow(
    "Petal brows",
    "ابروی گلبرگی",
    "M69 104 Q73 88 89 98 Q86 105 69 104Z",
    undefined,
    catInk,
  ),
  brow(
    "Tiny freckles",
    "خال ابرویی",
    "M73 102 Q84 98 95 102",
    g(c(69, 96, 1.7, catInk), c(78, 92, 1.5, catInk)),
  ),
  brow("Shy arch", "قوس خجالتی", "M68 105 Q87 103 99 94"),
  brow(
    "Cloud curl",
    "فر ابری",
    "M67 105 Q64 97 73 98 Q80 89 86 98 Q97 94 100 103",
  ),
  brow("Little wings", "بال ابرویی", "M67 105 Q77 103 81 94 Q85 101 99 100"),
  brow("Short long", "کوتاه و بلند", "M67 103 74 99 M81 98 Q91 96 101 102"),
  brow(
    "Dimple ends",
    "ابروی چال‌دار",
    "M68 103 Q83 93 98 103 M68 103 q-4 0 -3 5",
  ),
  brow(
    "Velvet brush",
    "ابروی مخملی",
    "M67 105 74 98 80 99 85 94 91 98 101 100 88 102 78 101Z",
    undefined,
    catInk,
  ),
  brow(
    "Wish star",
    "ستاره ابرویی",
    "M73 102 Q85 96 98 102",
    star(63, 100, gold),
  ),
  brow(
    "Leaf arches",
    "قوس برگی",
    "M68 104 Q76 88 96 99 Q83 109 68 104Z",
    p("M71 103 89 98", "none", 1),
    "#9271b9",
  ),
  brow(
    "Open curls",
    "فر باز",
    "M67 105 Q63 92 77 94 Q88 97 79 101 M87 100 101 103",
  ),
  brow("Soft chevrons", "هشتی نرم", "M68 104 83 96 99 104"),
  brow(
    "Twin petals",
    "دو گلبرگ",
    "M67 104 Q67 93 79 99 Q78 105 67 104Z M81 100 Q88 89 99 99 Q91 104 81 100Z",
    undefined,
    catInk,
  ),
  brow(
    "Sparked brow",
    "ابروی جرقه‌ای",
    "M73 103 Q86 96 99 102",
    g(p("M63 94 v7 m-4 -4 h8", "none", 1.8), c(68, 91, 1.5, catInk)),
  ),
  brow(
    "Fine braid",
    "ابروی بافته",
    "M67 103 Q73 96 79 102 T91 102 T103 100 M67 100 Q73 106 79 100 T91 100 T103 102",
  ),
  brow("Lazy commas", "ویرگول خوابالو", "M67 102 Q81 105 99 99 M67 102 l-2 -4"),
  brow(
    "Heart ends",
    "دل ابرویی",
    "M74 102 Q85 97 99 102",
    <g transform="translate(65 100) scale(.45)">{heart(0, 0, rose)}</g>,
  ),
  brow("Twin wisps", "دو پر نرم", "M66 105 Q78 95 88 101 M80 97 Q89 90 100 99"),
  brow(
    "Scalloped silk",
    "ابروی دالبری",
    "M66 104 Q70 95 76 101 Q82 92 88 100 Q95 94 101 103",
  ),
  brow(
    "Leaf tip",
    "نوک برگی",
    "M66 104 Q78 93 92 99",
    p("M91 99 q1 -10 10 -6 q-1 8 -10 6Z", mint, 1.4),
  ),
  brow(
    "Soft brackets",
    "ابروی پرانتزی",
    "M71 105 Q65 98 74 95 M82 98 Q92 95 101 102",
  ),
  brow(
    "Sun freckles",
    "خال آفتابی",
    "M71 102 Q84 95 98 102",
    g(c(63, 96, 2, gold), c(69, 91, 1.6, gold), c(77, 89, 1.3, gold)),
  ),
  brow("Ripple brows", "ابروی موج‌ریز", "M66 103 q5 -6 10 0 t10 0 t10 0"),
  brow(
    "Long tuft",
    "پشم بلند ابرو",
    "M66 105 76 94 80 102 87 91 92 101 101 102",
  ),
  brow(
    "Double commas",
    "دو ویرگول",
    "M67 104 Q66 94 78 97 Q76 104 67 104Z M84 101 Q86 92 99 97 Q94 104 84 101Z",
    undefined,
    catInk,
  ),
  brow("Tender curve", "قوس لطیف", "M66 101 Q80 107 99 95 M67 101 q-2 -5 3 -7"),
  brow(
    "Small halo",
    "هاله ابرو",
    "M70 104 Q83 96 97 104",
    <ellipse
      cx="83"
      cy="94"
      rx="11"
      ry="3"
      fill="none"
      stroke={gold}
      strokeWidth="1.8"
    />,
  ),
  brow(
    "Rose brush",
    "برس گلبهی",
    "M67 104 Q81 92 99 101 L88 105 78 102Z",
    undefined,
    rose,
  ),
  brow(
    "Falling stars",
    "ستاره‌بارون",
    "M72 103 Q85 98 98 103",
    g(star(65, 96, gold), c(76, 89, 1.7, gold)),
  ),
  brow(
    "Fern brows",
    "ابروی سرخسی",
    "M66 105 Q79 96 99 100 M73 101 73 95 M80 98 82 91 M88 99 93 93 M78 100 82 105 M89 100 94 104",
  ),
  brow(
    "Happy crown",
    "تاج خندون",
    "M67 104 72 96 80 102 85 93 91 102 99 97 102 105",
  ),
];
const nose = (
  name: string,
  fa: string,
  outline: string,
  fill = catInk,
  detail?: ReactNode,
) =>
  d(
    name,
    fa,
    <g transform="translate(128 151)">
      {p(outline, fill, 1.5)}
      {detail}
    </g>,
  );
export const noseDesigns = [
  nose("Wishy triangle", "بینی ویشی", "M-6 0 H6 L0 8Z"),
  nose(
    "Rose heart",
    "قلب صورتی",
    "M0 8 C-20 -2 -6 -10 0 -3 C6 -10 20 -2 0 8Z",
    rose,
  ),
  nose(
    "Soft bean",
    "لوبیای نرم",
    "M-8 0 Q-7 -7 0 -3 Q7 -7 8 0 Q4 9 0 8 Q-4 9 -8 0Z",
    rose,
  ),
  nose("Gold diamond", "الماس طلایی", "M0 -5 7 1 0 9 -7 1Z", gold),
  nose(
    "Milk button",
    "دکمه شیری",
    "M-6 -2 Q0 -6 6 -2 V4 Q0 10 -6 4Z",
    white,
    g(c(-2, 1, 1, catInk), c(2, 1, 1, catInk)),
  ),
  nose(
    "Little peach",
    "هلوی کوچولو",
    "M0 8 C-16 2 -9 -10 0 -4 C9 -10 16 2 0 8Z",
    rose,
    p("M0 -3 v6", "none", 1),
  ),
  nose(
    "Velvet oval",
    "بیضی مخملی",
    "M-8 0 C-8 -7 8 -7 8 0 Q7 7 0 8 Q-7 7 -8 0Z",
    catInk,
    e(-2, -1, 2, 1, white),
  ),
  nose(
    "Butterfly nose",
    "بینی پروانه‌ای",
    "M0 1 Q-12 -9 -8 3 Q-5 7 0 4 Q5 7 8 3 Q12 -9 0 1Z",
    rose,
  ),
  nose(
    "Acorn",
    "بلوطی",
    "M-7 0 Q0 -5 7 0 Q6 7 0 9 Q-6 7 -7 0Z",
    gold,
    p("M-7 0 Q0 3 7 0", "none", 1.5),
  ),
  nose("Petal tip", "نوک گلبرگ", "M0 -5 Q14 3 0 9 Q-14 3 0 -5Z", rose),
  nose(
    "Pink triangle",
    "مثلث صورتی",
    "M-8 -1 Q0 -5 8 -1 L0 8Z",
    rose,
    e(-2, -1, 2, 1, white),
  ),
  nose(
    "Split heart",
    "قلب دوتایی",
    "M0 8 C-18 -2 -6 -9 0 -3 C6 -9 18 -2 0 8Z",
    catInk,
    heart(-1, -1, rose),
  ),
  nose(
    "Tiny paw",
    "پنجه کوچولو",
    "M-6 2 Q0 -4 6 2 Q9 9 0 6 Q-9 9 -6 2Z",
    rose,
    g(c(-6, -3, 2, rose), c(0, -5, 2, rose), c(6, -3, 2, rose)),
  ),
  nose(
    "Sweet strawberry",
    "توت‌فرنگی",
    "M-8 -1 Q0 -6 8 -1 Q7 6 0 9 Q-7 6 -8 -1Z",
    rose,
    g(c(-3, 1, 0.8, catInk), c(3, 1, 0.8, catInk), c(0, 5, 0.8, catInk)),
  ),
  nose(
    "Rounded diamond",
    "لوزی گرد",
    "M0 -5 Q9 -1 7 3 L0 9 -7 3 Q-9 -1 0 -5Z",
    catInk,
    p("M-2 -2 1 -3", white, 1),
  ),
  nose(
    "Moon button",
    "دکمه ماهی",
    "M-7 0 Q0 -7 7 0 Q5 8 0 8 Q-5 8 -7 0Z",
    lilac,
    p("M-3 -1 Q-6 4 -1 5 Q-3 2 -1 0Z", white, 0),
  ),
  nose(
    "Soft trapezoid",
    "ذوزنقه نرم",
    "M-8 -2 Q0 -4 8 -2 L5 5 Q0 9 -5 5Z",
    rose,
  ),
  nose(
    "Kitten bow",
    "پاپیون بینی",
    "M0 1 -8 -4 -8 5 0 3 8 5 8 -4Z",
    catInk,
    c(0, 2, 2, rose),
  ),
  nose(
    "Honey drop",
    "قطره عسلی",
    "M0 -5 Q13 4 0 9 Q-13 4 0 -5Z",
    gold,
    e(-2, 0, 1.5, 2, white),
  ),
  nose(
    "Mint bean",
    "لوبیای نعنایی",
    "M-8 0 Q-6 -6 0 -3 Q6 -6 8 0 Q6 8 0 8 Q-6 8 -8 0Z",
    mint,
    p("M-3 -1 h3", white, 1),
  ),
  nose(
    "Freckled triangle",
    "مثلث خال‌دار",
    "M-7 -1 H7 Q4 7 0 8 Q-4 7 -7 -1Z",
    rose,
    g(
      c(-11, 2, 1, catInk),
      c(11, 2, 1, catInk),
      c(-14, -1, 1, catInk),
      c(14, -1, 1, catInk),
    ),
  ),
  nose(
    "Little tulip",
    "لاله کوچولو",
    "M-7 -4 -3 -1 0 -5 3 -1 7 -4 6 4 Q0 10 -6 4Z",
    rose,
  ),
  nose(
    "Cloud button",
    "دکمه ابری",
    "M-8 1 Q-10 -5 -4 -4 Q0 -9 4 -4 Q10 -5 8 1 Q4 9 0 8 Q-4 9 -8 1Z",
    white,
  ),
  nose(
    "Rosebud",
    "غنچه",
    "M-7 0 Q-5 -7 2 -5 Q10 -3 6 4 Q0 9 -6 4Z",
    rose,
    p("M-4 0 Q0 -4 4 0 Q1 5 -2 2Z", "none", 1),
  ),
  nose("Arrow tip", "نوک پیکانی", "M-8 -2 0 0 8 -2 0 9Z", catInk),
  nose(
    "Satin heart",
    "قلب ساتن",
    "M0 8 C-17 -1 -7 -10 0 -3 C7 -10 17 -1 0 8Z",
    rose,
    p("M-5 -2 Q-7 0 -4 2", white, 1.5),
  ),
  nose(
    "Dimple bean",
    "لوبیای چال‌دار",
    "M-8 -1 Q-4 -5 0 -2 Q4 -5 8 -1 Q6 8 0 8 Q-6 8 -8 -1Z",
    catInk,
    g(c(-3, 0, 1.3, rose), c(3, 0, 1.3, rose)),
  ),
  nose(
    "Wish gem",
    "نگین آرزو",
    "M0 -5 8 0 4 6 0 9 -4 6 -8 0Z",
    gold,
    p("M-8 0 H8 M0 -5 -4 6 0 9 4 6Z", "none", 0.8),
  ),
  nose(
    "Twin beans",
    "دو لوبیا",
    "M0 6 Q-9 9 -9 1 Q-6 -5 0 0 Q6 -5 9 1 Q9 9 0 6Z",
    rose,
    p("M0 0 v6", "none", 1),
  ),
  nose(
    "Apple nose",
    "بینی سیبی",
    "M0 -2 Q-11 -8 -9 2 Q-8 10 0 7 Q8 10 9 2 Q11 -8 0 -2Z",
    rose,
    p("M0 -2 2 -6", "none", 1.5),
  ),
  nose(
    "Velvet cushion",
    "کوسن مخملی",
    "M-8 -2 Q0 -6 8 -2 V4 L0 8 -8 4Z",
    catInk,
    p("M-4 -1 H1", white, 1),
  ),
  nose(
    "Petal pair",
    "دو گلبرگ",
    "M0 7 Q-14 4 -7 -4 Q0 -6 0 1 Q0 -6 7 -4 Q14 4 0 7Z",
    rose,
  ),
  nose(
    "Sunny button",
    "دکمه آفتابی",
    "M-7 0 Q-4 -7 3 -4 Q10 -1 6 5 Q0 11 -6 5Z",
    gold,
    c(-2, 0, 2, white),
  ),
  nose(
    "Cat nose slit",
    "بینی خط‌دار",
    "M-8 -1 Q0 -6 8 -1 Q7 6 0 8 Q-7 6 -8 -1Z",
    rose,
    p("M0 -1 v5", "none", 1.5),
  ),
  nose(
    "Little shell",
    "صدف کوچولو",
    "M-8 1 Q-9 -5 -4 -4 Q0 -8 4 -4 Q9 -5 8 1 L0 8Z",
    rose,
    p("M-4 -2 0 7 4 -2 M0 -4 v11", "none", 0.9),
  ),
  nose(
    "Moon tip",
    "نوک هلالی",
    "M-8 -2 Q0 5 8 -2 Q7 6 0 9 Q-7 6 -8 -2Z",
    catInk,
  ),
  nose(
    "Pearl heart",
    "قلب مرواریدی",
    "M0 8 C-17 -1 -7 -9 0 -3 C7 -9 17 -1 0 8Z",
    white,
    c(-4, -1, 1.5, rose),
  ),
  nose(
    "Maple petal",
    "برگ افرا",
    "M0 -5 3 -1 7 -3 6 1 9 3 3 6 0 9 -3 6 -9 3 -6 1 -7 -3 -3 -1Z",
    gold,
  ),
  nose(
    "Round triangle",
    "مثلث گرد",
    "M-7 -2 Q-10 -2 -7 2 L-2 8 Q0 10 2 8 L7 2 Q10 -2 7 -2Z",
    rose,
  ),
  nose(
    "Split diamond",
    "الماس دو رنگ",
    "M0 -5 7 1 0 9 -7 1Z",
    lilac,
    p("M0 -5 7 1 0 9Z", rose, 0),
  ),
  nose(
    "Poppy seed",
    "دونه خشخاش",
    "M-7 0 Q-5 -6 0 -3 Q5 -6 7 0 Q5 7 0 8 Q-5 7 -7 0Z",
    catInk,
    g(c(-3, -1, 1, white), c(2, 2, 1, white)),
  ),
  nose(
    "Daisy button",
    "دکمه بابونه",
    "M-7 0 Q-8 -5 -3 -4 Q0 -8 3 -4 Q8 -5 7 0 Q10 4 5 6 Q0 11 -5 6 Q-10 4 -7 0Z",
    white,
    c(0, 2, 2.5, gold),
  ),
  nose(
    "Silk knot",
    "گره ابریشمی",
    "M-8 -2 Q0 -6 8 -2 L4 5 0 8 -4 5Z",
    rose,
    p("M-4 -1 0 6 4 -1", "none", 0.9),
  ),
  nose(
    "Lucky clover",
    "شبدر شانس",
    "M0 7 Q-11 5 -8 -1 Q-5 -6 0 -2 Q5 -6 8 -1 Q11 5 0 7Z",
    mint,
    p("M0 -2 v8", "none", 1),
  ),
  nose(
    "Tiny star",
    "ستاره کوچولو",
    "M0 -6 3 -1 8 0 4 4 4 8 0 6 -4 8 -4 4 -8 0 -3 -1Z",
    gold,
  ),
  nose(
    "Dotted heart",
    "قلب خال‌دار",
    "M0 8 C-17 -1 -7 -9 0 -3 C7 -9 17 -1 0 8Z",
    rose,
    g(c(-3, -1, 0.9, white), c(3, -1, 0.9, white), c(0, 3, 0.9, white)),
  ),
  nose("Gentle chevron", "هشتی لطیف", "M-8 -3 0 1 8 -3 5 4 0 9 -5 4Z", rose),
  nose(
    "Cocoa bean",
    "لوبیای کاکائویی",
    "M-7 0 Q-6 -6 1 -5 Q9 -4 8 2 Q5 10 -2 7 Q-8 5 -7 0Z",
    catInk,
    p("M1 -4 Q-3 1 1 6", "none", 1.2),
  ),
  nose(
    "Buttercup button",
    "دکمه آلاله",
    "M-7 0 Q-8 -6 -2 -4 Q2 -9 5 -3 Q11 -2 7 3 Q6 10 0 7 Q-7 9 -7 0Z",
    gold,
    c(-2, 0, 1.8, white),
  ),
  nose(
    "Wish shine",
    "برق آرزو",
    "M-8 -1 Q0 -5 8 -1 L0 9Z",
    catInk,
    g(p("M-3 -1 h5", white, 1), c(-11, -4, 1, gold), c(11, -4, 1, gold)),
  ),
];

const mouth = (name: string, fa: string, art: ReactNode) =>
  d(name, fa, <g transform="translate(128 164)">{art}</g>);
const smile = (outline: string) => p(outline, "none", 2.5);
const tongue = (outline: string) => p(outline, rose, 1.3);
const tooth = (outline: string) => p(outline, white, 1.2);
export const mouthDesigns = [
  mouth(
    "Wishy smile",
    "لبخند ویشی",
    smile("M0 -5 V8 Q-7 16 -14 9 M0 8 Q7 16 14 9"),
  ),
  mouth(
    "Tiny blep",
    "نوک زبون",
    g(
      smile("M0 -5 V7 Q-7 13 -13 7 M0 7 Q7 13 13 7"),
      tongue("M-5 11 H5 V17 Q0 23 -5 17Z"),
      p("M0 12 v5", "none", 1),
    ),
  ),
  mouth(
    "Happy bean",
    "لبخند لوبیایی",
    g(
      p("M-12 10 Q0 17 12 10 Q10 28 0 27 Q-10 28 -12 10Z", catInk, 2),
      tongue("M-7 22 Q0 17 7 22 Q0 29 -7 22Z"),
    ),
  ),
  mouth(
    "One fang",
    "یک نیش کوچولو",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      tooth("M6 12 10 19 12 10Z"),
    ),
  ),
  mouth(
    "Two fangs",
    "دوتا نیش",
    g(
      smile("M0 -5 V7 Q-7 15 -14 8 M0 7 Q7 15 14 8"),
      tooth("M-12 10 -10 18 -6 12Z M6 12 10 18 12 10Z"),
    ),
  ),
  mouth(
    "Shy smile",
    "لبخند خجالتی",
    g(
      smile("M-11 10 Q0 21 11 10"),
      c(-15, 10, 1.5, catInk),
      c(15, 10, 1.5, catInk),
    ),
  ),
  mouth(
    "Little o",
    "اوی کوچولو",
    g(
      smile("M0 -5 V2"),
      p("M0 6 C-10 6 -10 23 0 23 C10 23 10 6 0 6Z", catInk, 1.5),
      e(-2, 11, 2, 1, white),
    ),
  ),
  mouth(
    "Left smirk",
    "لبخند کج چپ",
    smile("M0 -5 V8 Q-7 16 -14 8 M0 8 Q7 12 13 9"),
  ),
  mouth(
    "Right smirk",
    "لبخند کج راست",
    smile("M0 -5 V8 Q-7 12 -13 9 M0 8 Q7 16 14 8"),
  ),
  mouth(
    "Heart laugh",
    "خنده قلبی",
    g(
      p("M-12 9 Q-4 6 0 12 Q4 6 12 9 Q13 21 0 29 Q-13 21 -12 9Z", catInk, 1.7),
      tongue("M-7 22 Q0 17 7 22 L0 27Z"),
    ),
  ),
  mouth(
    "Double dimples",
    "دو چال لبخند",
    g(smile("M-13 10 Q0 24 13 10 M-13 8 q-5 1 -3 6 M13 8 q5 1 3 6")),
  ),
  mouth(
    "Tiny teeth",
    "دندون ریز",
    g(
      p("M-13 10 Q0 14 13 10 Q9 25 0 25 Q-9 25 -13 10Z", catInk, 1.8),
      tooth("M-10 11 Q0 15 10 11 L7 16 H-7Z"),
    ),
  ),
  mouth(
    "Cat curl",
    "فر گربه‌ای",
    smile("M0 -5 V8 Q-11 20 -15 10 Q-15 5 -10 8 M0 8 Q11 20 15 10 Q15 5 10 8"),
  ),
  mouth(
    "Milk moustache",
    "سبیل شیری",
    g(
      p(
        "M0 7 Q-5 2 -12 8 Q-16 18 -5 15 L0 11 5 15 Q16 18 12 8 Q5 2 0 7Z",
        white,
        1.3,
      ),
      smile("M0 -5 V8 Q-6 15 -12 9 M0 8 Q6 15 12 9"),
    ),
  ),
  mouth(
    "Side blep",
    "زبون کجکی",
    g(
      smile("M0 -5 V8 Q-7 14 -13 8 M0 8 Q6 14 13 7"),
      tongue("M4 12 Q16 9 13 20 Q7 25 4 12Z"),
    ),
  ),
  mouth("Soft w", "دبلیوی نرم", smile("M-14 9 Q-9 22 0 10 Q9 22 14 9")),
  mouth(
    "Singing",
    "آوازخون",
    g(
      p("M0 6 Q-10 6 -8 20 Q0 31 8 20 Q10 6 0 6Z", catInk, 1.7),
      tongue("M-6 21 Q0 17 6 21 Q0 27 -6 21Z"),
    ),
  ),
  mouth("Little kiss", "بوس کوچولو", smile("M-5 7 Q9 5 3 12 Q11 16 -3 19")),
  mouth(
    "Cheeky tooth",
    "دندون شیطون",
    g(smile("M-14 10 Q0 24 14 7"), tooth("M-10 13 -6 21 -2 16Z")),
  ),
  mouth(
    "Lower lip",
    "لب کوچولو",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      p("M-4 21 Q0 23 4 21", "none", 1.4),
    ),
  ),
  mouth(
    "Bean blep",
    "زبون لوبیایی",
    g(
      smile("M0 -5 V8 Q-6 14 -12 8 M0 8 Q6 14 12 8"),
      tongue("M-6 12 Q2 10 5 14 Q8 23 0 24 Q-7 24 -6 12Z"),
    ),
  ),
  mouth(
    "Wide giggle",
    "خنده ریزریز",
    g(
      p("M-15 12 Q0 18 15 12 Q12 28 0 28 Q-12 28 -15 12Z", catInk, 1.8),
      tooth("M-11 14 Q0 18 11 14 L9 18 Q0 21 -9 18Z"),
      tongue("M-6 25 Q0 21 6 25Z"),
    ),
  ),
  mouth(
    "Comfy curl",
    "فر آروم",
    smile("M0 -5 V9 Q-5 18 -12 12 Q-16 5 -9 8 M0 9 Q5 18 12 12 Q16 5 9 8"),
  ),
  mouth(
    "Peach pout",
    "لب هلویی",
    g(
      p("M-7 10 Q0 5 7 10 Q0 22 -7 10Z", rose, 1.5),
      p("M-6 11 h12", "none", 1),
    ),
  ),
  mouth(
    "Dimple blep",
    "زبون چال‌دار",
    g(
      smile("M-13 10 Q0 19 13 10 M-15 9 l-1 4 M15 9 l1 4"),
      tongue("M-4 15 H4 V20 Q0 25 -4 20Z"),
    ),
  ),
  mouth(
    "Little yawn",
    "خمیازه کوچولو",
    g(
      smile("M0 -5 V1"),
      p("M-6 6 Q0 1 6 6 L7 21 Q0 32 -7 21Z", catInk, 1.5),
      tongue("M-5 22 Q0 18 5 22 Q0 28 -5 22Z"),
    ),
  ),
  mouth(
    "Cat moustache",
    "سبیل فرخورده",
    smile(
      "M0 -5 V8 Q-7 17 -13 12 Q-20 7 -13 5 Q-8 5 -10 9 M0 8 Q7 17 13 12 Q20 7 13 5 Q8 5 10 9",
    ),
  ),
  mouth(
    "Tiny grin",
    "پوزخند کوچولو",
    g(
      p("M-13 10 Q0 20 13 10 L9 19 Q0 25 -9 19Z", white, 1.8),
      p("M0 15 v7", "none", 1.1),
    ),
  ),
  mouth(
    "Rose smile",
    "لبخند گلبهی",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      p("M-5 19 Q0 24 5 19 Q0 28 -5 19Z", rose, 0),
    ),
  ),
  mouth(
    "Bunny teeth",
    "دندون خرگوشی",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      tooth("M-5 13 H5 V21 H-5Z"),
      p("M0 14 v6", "none", 1),
    ),
  ),
  mouth(
    "Shy curl",
    "فر خجالتی",
    g(
      smile("M-12 10 Q0 22 12 10"),
      p("M-14 8 q-4 3 0 6 M14 8 q4 3 0 6", "none", 1.4),
    ),
  ),
  mouth(
    "Tiny heart lip",
    "لب قلبی",
    g(
      smile("M0 -5 V6"),
      <g transform="translate(0 14) scale(.65)">{heart(0, 0, rose)}</g>,
    ),
  ),
  mouth(
    "Sleepy smile",
    "لبخند خوابالو",
    g(
      smile("M0 -5 V8 Q-7 13 -14 9 M0 8 Q7 13 14 9"),
      p("M-7 18 Q0 20 7 18", "none", 1.2),
    ),
  ),
  mouth(
    "Happy fang laugh",
    "خنده نیش‌دار",
    g(
      p("M-13 10 Q0 17 13 10 Q12 27 0 27 Q-12 27 -13 10Z", catInk, 1.8),
      tooth("M-10 12 -8 20 -3 15Z M3 15 8 20 10 12Z"),
      tongue("M-5 24 Q0 20 5 24Z"),
    ),
  ),
  mouth(
    "Crescent laugh",
    "خنده هلالی",
    g(
      p("M-14 12 Q0 29 14 12 Q7 32 -5 25Z", catInk, 1.7),
      tooth("M-10 16 Q0 26 10 16 Q1 29 -10 16Z"),
    ),
  ),
  mouth(
    "Tiny tongue curl",
    "زبون فرخورده",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      tongue("M-4 13 H4 V20 Q-2 28 -7 20 Q-8 14 -3 17"),
    ),
  ),
  mouth(
    "Soft zigzag",
    "لبخند شکسته نرم",
    smile("M-14 10  -8 15 0 10 8 15 14 10"),
  ),
  mouth(
    "Cheek dots",
    "لبخند خال‌دار",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      c(-17, 15, 1.2, catInk),
      c(17, 15, 1.2, catInk),
    ),
  ),
  mouth(
    "Playful pout",
    "لب شیطون",
    g(
      smile("M0 -5 V7 Q-7 17 -13 9 M0 7 Q7 10 13 6"),
      tongue("M-3 14 Q4 11 7 17 Q3 24 -3 20Z"),
    ),
  ),
  mouth(
    "Half grin",
    "نیم‌خنده",
    g(smile("M-13 12 Q2 21 14 6"), tooth("M5 14 7 19 11 10Z")),
  ),
  mouth(
    "Little whistle",
    "سوت کوچولو",
    g(
      smile("M0 -5 V1"),
      p("M-5 9 Q0 5 5 9 Q0 15 -5 9Z", catInk, 1.5),
      p("M8 9 12 7 M8 13 12 15", "none", 1.1),
    ),
  ),
  mouth(
    "Heart blep",
    "زبون قلبی",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      tongue("M-6 14 Q0 11 6 14 Q7 24 0 25 Q-7 24 -6 14Z"),
      p("M0 17 v5", "none", 1),
    ),
  ),
  mouth(
    "Soft oval laugh",
    "خنده بیضی",
    g(
      e(0, 15, 10, 11, catInk),
      tooth("M-7 8 Q0 5 7 8 L6 12 H-6Z"),
      tongue("M-6 22 Q0 17 6 22Z"),
    ),
  ),
  mouth(
    "Twin cheek curls",
    "دو فر لبخند",
    g(
      smile(
        "M-11 12 Q0 22 11 12 M-11 12 q-10 0 -6 -7 q5 -2 4 3 M11 12 q10 0 6 -7 q-5 -2 -4 3",
      ),
    ),
  ),
  mouth(
    "Tiny sleepy blep",
    "زبون خوابالو",
    g(smile("M-12 10 Q0 14 12 10"), tongue("M-5 12 H5 V17 Q0 22 -5 17Z")),
  ),
  mouth(
    "Two dimples and lip",
    "چال و لب کوچولو",
    g(
      smile("M-12 10 Q0 21 12 10 M-15 10 v4 M15 10 v4"),
      p("M-3 23 h6", "none", 1.3),
    ),
  ),
  mouth(
    "Kitten squeak",
    "میوی کوچولو",
    g(
      smile("M0 -5 V3"),
      p("M0 6 -8 14 0 25 8 14Z", catInk, 1.8),
      tongue("M-4 20 Q0 15 4 20 L0 24Z"),
    ),
  ),
  mouth(
    "Milk lip",
    "لب شیری",
    g(
      smile("M0 -5 V8 Q-7 15 -14 8 M0 8 Q7 15 14 8"),
      p("M-6 20 Q0 25 6 20 Q0 29 -6 20Z", white, 1),
    ),
  ),
  mouth(
    "Bean grin",
    "خنده لوبیایی",
    g(
      p("M-13 10 Q0 16 13 10 Q15 24 2 27 Q-13 29 -13 10Z", catInk, 1.8),
      tooth("M-10 12 Q0 17 10 12 L8 17 Q0 20 -8 17Z"),
      tongue("M-5 24 Q2 20 8 23 Q1 28 -5 24Z"),
    ),
  ),
  mouth(
    "Wishful smile",
    "لبخند آرزو",
    g(
      smile("M0 -5 V8 Q-9 18 -15 8 M0 8 Q9 18 15 8"),
      p("M-4 23 Q0 25 4 23", "none", 1.2),
    ),
  ),
];
const whisk = (name: string, fa: string, outline: string, detail?: ReactNode) =>
  d(name, fa, mirror(g(p(outline, "none", 1.8), detail)));
export const whiskerDesigns = [
  d("Logo cheeks", "گونه‌های لوگو", null),
  whisk(
    "Soft three",
    "سه تار نرم",
    "M63 184 Q44 177 28 179 M62 190 H25 M65 196 Q44 199 30 207",
  ),
  whisk("Fine pair", "دو تار ظریف", "M61 186 29 183 M64 194 31 201"),
  whisk(
    "Upward sweep",
    "سبیل رو به بالا",
    "M62 185 Q39 184 26 172 M63 192 Q39 194 25 188",
  ),
  whisk(
    "Downward sweep",
    "سبیل رو به پایین",
    "M63 184 Q43 184 29 191 M64 191 Q42 199 31 211",
  ),
  whisk(
    "Tiny curls",
    "فر ریز",
    "M62 184 Q28 175 29 186 M64 194 Q28 193 33 206",
  ),
  whisk(
    "Dotted roots",
    "ریشه خال‌دار",
    "M60 186 27 181 M63 196 30 203",
    g(
      c(68, 184, 1.7, catInk),
      c(70, 191, 1.7, catInk),
      c(74, 186, 1.7, catInk),
    ),
  ),
  whisk(
    "Four fans",
    "چهار تار بادبزنی",
    "M63 182 32 172 M61 187 25 183 M62 193 25 197 M66 198 34 214",
  ),
  whisk(
    "Little commas",
    "سبیل ویرگولی",
    "M62 186 Q34 177 28 185 Q25 190 32 188 M64 195 Q34 196 32 205 Q34 210 37 205",
  ),
  whisk(
    "Ribbon whiskers",
    "سبیل روبانی",
    "M62 185 Q45 176 28 182 Q37 187 48 184 M64 194 Q45 205 29 201",
  ),
  whisk(
    "Three freckles",
    "سه خال",
    "",
    g(c(63, 186, 2, catInk), c(72, 188, 2, catInk), c(65, 196, 2, catInk)),
  ),
  whisk(
    "Broken lines",
    "خط‌های تکه‌ای",
    "M62 186 48 182 M42 181 27 180 M64 195 48 198 M42 200 31 204",
  ),
  whisk(
    "Leaf tips",
    "نوک برگی",
    "M62 185 Q42 180 29 175 M64 195 Q45 198 32 208",
    g(
      p("M29 175 q-9 -10 -7 0 q5 5 7 0Z", mint, 1),
      p("M32 208 q-9 -3 -6 6 q7 2 6 -6Z", mint, 1),
    ),
  ),
  whisk(
    "Bouncy pair",
    "دو تار فنری",
    "M62 185 Q48 176 41 183 T26 180 M64 195 Q49 202 42 198 T29 206",
  ),
  whisk(
    "Short brush",
    "برس کوچولو",
    "M63 183 43 179 M61 188 37 187 M63 193 40 197 M66 198 48 205",
  ),
  whisk(
    "Twin loops",
    "دو حلقه",
    "M62 185 Q33 175 27 186 Q25 196 40 188 M64 195 Q34 192 31 204 Q32 214 44 202",
  ),
  whisk(
    "Star tips",
    "نوک ستاره‌ای",
    "M62 186 33 180 M64 195 35 207",
    g(star(28, 178, gold), c(31, 210, 2, gold)),
  ),
  whisk(
    "Tapered fur",
    "سبیل پشمی",
    "M63 184 32 174 48 184 28 185 62 190 M64 195 29 204 49 200 38 214",
  ),
  whisk(
    "Satin arcs",
    "قوس ساتن",
    "M62 184 Q44 170 25 176 M63 191 Q41 185 24 191 M66 198 Q44 201 31 213",
  ),
  whisk(
    "Cheek dashes",
    "خط گونه‌ای",
    "M64 184 56 181 M67 191 57 191 M71 198 62 202",
  ),
  whisk(
    "Freckle fan",
    "خال بادبزنی",
    "M62 185 30 177 M63 192 27 193 M66 198 35 210",
    g(
      c(70, 184, 1.3, catInk),
      c(73, 191, 1.3, catInk),
      c(77, 187, 1.3, catInk),
    ),
  ),
  whisk(
    "Long curl",
    "فر بلند",
    "M63 186 Q26 169 23 186 Q23 196 33 189 M65 196 Q33 200 35 211",
  ),
  whisk(
    "Upturned pair",
    "دو تار برگشته",
    "M62 185 Q33 187 27 172 M64 195 Q34 203 26 190",
  ),
  whisk(
    "Downturned pair",
    "دو تار افتاده",
    "M62 185 Q33 174 25 188 M64 195 Q36 193 30 211",
  ),
  whisk(
    "Double tips",
    "نوک دوشاخه",
    "M62 186 31 181 25 175 M31 181 24 185 M64 195 35 203 30 210 M35 203 27 201",
  ),
  whisk(
    "Wave trio",
    "سه موج",
    "M63 182 q-9 -9 -18 -4 t-17 -3 M62 190 q-10 -5 -18 0 t-18 0 M65 198 q-10 6 -18 4 t-14 8",
  ),
  whisk(
    "Soft roots",
    "ریشه پشمی",
    "M63 184 54 180 58 185 28 179 M64 195 55 197 59 193 30 205",
  ),
  whisk(
    "Rosy freckles",
    "خال صورتی",
    "M62 185 29 181 M64 195 32 205",
    g(c(69, 187, 2, rose), c(75, 189, 2, rose), c(71, 195, 2, rose)),
  ),
  whisk(
    "Crescent ends",
    "نوک هلالی",
    "M62 185 Q32 172 27 184 Q26 190 31 191 M64 195 Q37 198 34 208 Q34 212 39 212",
  ),
  whisk(
    "Two long one short",
    "دو بلند یک کوتاه",
    "M62 183 27 172 M61 190 43 189 M65 198 30 210",
  ),
  whisk(
    "Crossed wisps",
    "تارهای ضربدری",
    "M63 183 28 190 M62 192 30 178 M66 199 32 208",
  ),
  whisk(
    "Puffy cheeks",
    "سبیل پفکی",
    "M62 185 Q50 180 45 185 Q37 179 30 183 M64 195 Q50 200 44 197 Q36 206 30 203",
  ),
  whisk(
    "Gentle brackets",
    "پرانتز مهربون",
    "M62 186 Q39 177 31 180 L28 185 M64 195 Q42 204 34 204 L31 199",
  ),
  whisk(
    "Three tiny ticks",
    "سه خط ریز",
    "M64 184 52 178 M65 191 50 190 M70 198 57 205",
  ),
  whisk(
    "Dotted trails",
    "رد نقطه‌ای",
    "M62 186 44 182 M64 195 46 200",
    g(
      c(37, 180, 1.5, catInk),
      c(30, 179, 1.2, catInk),
      c(39, 203, 1.5, catInk),
      c(33, 206, 1.2, catInk),
    ),
  ),
  whisk(
    "Spring coils",
    "فنر کوچولو",
    "M62 185 Q35 173 27 182 Q23 190 31 190 Q37 187 30 184 M64 195 Q38 196 33 205 Q32 214 39 209",
  ),
  whisk(
    "Feather split",
    "شاخه پری",
    "M62 185 29 177 M46 181 39 172 M64 195 32 207 M47 201 42 212",
  ),
  whisk(
    "Lucky dots",
    "خال خوش‌شانس",
    "M62 186 31 181 M64 195 34 206",
    g(c(70, 185, 2, gold), c(75, 190, 1.5, gold), c(69, 195, 1.5, gold)),
  ),
  whisk(
    "Long low fan",
    "بادبزن پایینی",
    "M62 186 Q39 184 26 188 M64 193 Q41 198 29 205 M68 199 Q49 208 40 218",
  ),
  whisk(
    "High fan",
    "بادبزن بالایی",
    "M62 183 Q37 175 28 165 M61 189 Q36 186 25 177 M65 197 Q39 199 27 192",
  ),
  whisk(
    "Little zigzags",
    "زیگزاگ ریز",
    "M63 185 48 180 44 184 28 179 M64 195 49 201 44 198 31 207",
  ),
  whisk(
    "Milky roots",
    "ریشه شیری",
    "M62 185 28 179 M64 195 31 206",
    g(c(69, 185, 1.7, white), c(74, 190, 1.7, white), c(69, 195, 1.7, white)),
  ),
  whisk(
    "Half loops",
    "نیم‌حلقه",
    "M62 185 Q39 176 29 184 Q33 191 40 186 M64 195 Q41 194 33 204 Q40 209 44 202",
  ),
  whisk(
    "Ribbon ends",
    "نوک روبانی",
    "M62 185 29 178 32 185 M29 178 23 181 M64 195 33 206 40 206 M33 206 34 213",
  ),
  whisk(
    "Twin stars",
    "دو ستاره",
    "M62 186 37 180 M64 196 38 207",
    g(star(30, 177, white), star(32, 212, gold)),
  ),
  whisk(
    "Fur fans",
    "بادبزن پشمی",
    "M63 184 33 174 39 182 25 183 44 188 62 190 M64 195 38 200 26 210 42 208 39 216",
  ),
  whisk(
    "Quiet curls",
    "فر آروم",
    "M62 186 Q39 178 30 185 M64 195 Q38 200 35 209 Q37 214 41 208 M63 191 43 190",
  ),
  whisk(
    "Whisker spark",
    "جرقه سبیل",
    "M62 185 31 178 M64 195 33 206",
    g(p("M24 171 v8 m-4 -4 h8", "none", 1.4), c(28, 211, 1.8, gold)),
  ),
  whisk(
    "Five freckles",
    "پنج خال",
    "M62 186 37 181 M64 196 38 206",
    g(
      c(68, 184, 1.4, catInk),
      c(74, 185, 1.4, catInk),
      c(70, 191, 1.4, catInk),
      c(77, 191, 1.4, catInk),
      c(73, 197, 1.4, catInk),
    ),
  ),
  whisk(
    "Wishy wisps",
    "تارهای ویشی",
    "M62 183 Q42 172 27 178 M61 190 Q39 186 24 192 M64 197 Q43 202 33 214",
    g(p("M49 180 44 173 M47 204 45 211", "none", 1.3)),
  ),
];

const mark = (name: string, fa: string, art: ReactNode) => d(name, fa, art);
const shade = (art: ReactNode) => (
  <g fill={catInk} opacity=".2">
    {art}
  </g>
);
const cream = (art: ReactNode) => (
  <g fill="#fff3df" opacity=".55">
    {art}
  </g>
);
const raw = (outline: string) => <path d={outline} />;
const spots = (points: number[][], fill = catInk, opacity = 0.22) => (
  <g fill={fill} opacity={opacity}>
    {points.map(([x, y, r], i) => (
      <circle key={i} cx={x} cy={y} r={r} />
    ))}
  </g>
);
export const markingDesigns = [
  mark(
    "Wish gem",
    "نگین ویشی",
    g(
      p("M128 95 139 116 128 134 117 116Z", gold, 0),
      p("M128 101 134 116 128 127 122 116Z", "#ffda52", 0),
    ),
  ),
  mark("Bare fur", "پشم ساده", null),
  mark(
    "Classic tabby",
    "راه‌راه کلاسیک",
    shade(
      raw(
        "M109 76 112 101 117 106 120 75Z M123 73 126 109 131 109 135 73Z M139 75 141 105 147 100 149 76Z",
      ),
    ),
  ),
  mark(
    "Milk blaze",
    "لکه شیری",
    cream(
      raw(
        "M121 74 Q113 95 118 116 L124 151 Q113 177 104 190 Q128 208 152 190 Q143 177 132 151 L138 116 Q143 95 135 74Z",
      ),
    ),
  ),
  mark(
    "Tuxedo bib",
    "پیش‌بند سفید",
    cream(
      raw(
        "M68 196 Q89 188 107 197 Q128 208 149 197 Q167 188 188 196 L166 226 H90Z",
      ),
    ),
  ),
  mark(
    "Calico sweep",
    "خال سه‌رنگ",
    g(
      shade(raw("M39 83 Q75 66 101 82 Q93 111 65 126 L39 121Z")),
      cream(
        raw("M173 178 Q204 170 214 189 L204 218 167 224 Q157 199 173 178Z"),
      ),
    ),
  ),
  mark("Forehead heart", "قلب پیشونی", heart(128, 103, gold)),
  mark(
    "Moon mark",
    "لکه ماه",
    p("M132 88 Q111 100 129 119 Q119 101 140 98Z", gold, 0),
  ),
  mark(
    "Tiger cheeks",
    "گونه ببری",
    shade(
      raw(
        "M40 173 65 180 43 184Z M48 190 78 195 56 202Z M216 173 191 180 213 184Z M208 190 178 195 200 202Z",
      ),
    ),
  ),
  mark(
    "Soft freckles",
    "خال ریز",
    spots([
      [69, 189, 2],
      [78, 194, 2],
      [73, 201, 1.8],
      [187, 189, 2],
      [178, 194, 2],
      [183, 201, 1.8],
    ]),
  ),
  mark(
    "Split mask",
    "ماسک دو رنگ",
    shade(raw("M128 64 Q100 91 106 124 L119 159 105 219 H38 V67Z")),
  ),
  mark(
    "Snow cap",
    "کلاه برفی",
    cream(
      raw(
        "M65 76 Q128 55 191 76 L184 98 166 91 151 99 137 90 123 100 106 92 87 100 72 91Z",
      ),
    ),
  ),
  mark(
    "Rosy cheeks",
    "لپ گلی",
    g(e(67, 192, 12, 7, rose), e(189, 192, 12, 7, rose)),
  ),
  mark(
    "Three diamonds",
    "سه لوزی",
    g(
      p("M128 86 135 99 128 112 121 99Z", gold, 0),
      p(
        "M107 91 111 98 107 105 103 98Z M149 91 153 98 149 105 145 98Z",
        gold,
        0,
      ),
    ),
  ),
  mark(
    "Cloud chin",
    "چونه ابری",
    cream(
      raw(
        "M86 206 Q92 192 106 201 Q115 188 128 200 Q141 188 150 201 Q164 192 170 206 L156 226 H100Z",
      ),
    ),
  ),
  mark(
    "Little lightning",
    "برق کوچولو",
    p("M129 83 117 104 128 104 122 126 141 100 130 100 137 83Z", gold, 0),
  ),
  mark(
    "Bengal rosettes",
    "خال پلنگی",
    <g fill="none" stroke={catInk} strokeWidth="3" opacity=".2">
      <path d="M68 191 q-8 -5 -10 3 q3 8 10 4 m10 4 q-9 -4 -9 4 q2 7 10 2 M188 191 q8 -5 10 3 q-3 8 -10 4 m-10 4 q9 -4 9 4 q-2 7 -10 2" />
    </g>,
  ),
  mark(
    "Cinnamon cap",
    "کلاه دارچینی",
    shade(
      raw(
        "M48 92 Q78 69 105 73 L118 94 128 85 138 94 151 73 Q178 69 208 92 L183 111 160 104 146 114 128 103 110 114 96 104 73 111Z",
      ),
    ),
  ),
  mark(
    "Star forehead",
    "ستاره پیشونی",
    g(star(128, 104, gold), c(114, 89, 2, gold), c(142, 89, 2, gold)),
  ),
  mark(
    "Marble swirl",
    "رگه مرمری",
    <g fill="none" stroke={catInk} strokeWidth="5" opacity=".17">
      <path d="M75 87 Q95 69 106 88 Q110 105 94 103 M181 87 Q161 69 150 88 Q146 105 162 103 M108 210 Q128 195 148 210" />
    </g>,
  ),
  mark(
    "Butterfly blaze",
    "لکه پروانه‌ای",
    cream(
      raw(
        "M128 107 Q106 75 101 97 Q98 116 121 125 L128 152 135 125 Q158 116 155 97 Q150 75 128 107Z",
      ),
    ),
  ),
  mark(
    "Dot constellation",
    "صورت فلکی",
    g(
      spots(
        [
          [117, 91, 2],
          [129, 84, 2.5],
          [140, 97, 2],
          [125, 109, 2],
        ],
        gold,
        1,
      ),
      p("M117 91 129 84 140 97 125 109", "none", 0.8),
    ),
  ),
  mark(
    "Raccoon cap",
    "ماسک راکونی",
    shade(
      raw(
        "M47 97 Q87 82 113 109 L128 125 143 109 Q169 82 209 97 L211 151 Q178 171 146 149 L128 138 110 149 Q78 171 45 151Z",
      ),
    ),
  ),
  mark(
    "Cream muzzle",
    "پوزه خامه‌ای",
    cream(
      raw(
        "M107 168 Q118 160 128 170 Q138 160 149 168 Q164 181 149 197 Q128 207 107 197 Q92 181 107 168Z",
      ),
    ),
  ),
  mark(
    "Sun disk",
    "قرص آفتاب",
    g(
      c(128, 104, 10, gold),
      p("M128 88 v-4 m12 8 3 -3 m-27 3 -3 -3 m15 31 v4", "none", 1.5),
    ),
  ),
  mark(
    "Leaf forehead",
    "برگ پیشونی",
    g(
      p("M128 117 Q109 99 127 86 Q145 99 128 117Z", mint, 0),
      p("M128 111 V93", "none", 1.3),
    ),
  ),
  mark(
    "Tiger crown",
    "تاج ببری",
    shade(
      raw(
        "M92 81 102 102 111 106 108 79Z M118 74 124 103 128 113 132 103 138 74Z M148 79 145 106 154 102 164 81Z",
      ),
    ),
  ),
  mark("One heart cheek", "دل روی لپ", heart(184, 198, rose)),
  mark(
    "Peach blush",
    "رژگونه هلویی",
    g(
      e(68, 194, 13, 8, "#ed987e"),
      e(188, 194, 13, 8, "#ed987e"),
      p("M61 192 l-2 5 m9 -5 -2 5 m119 -5 -2 5 m9 -5 -2 5", "none", 1),
    ),
  ),
  mark(
    "Snow freckles",
    "خال برفی",
    spots(
      [
        [115, 88, 2],
        [128, 95, 2.8],
        [141, 88, 2],
        [64, 192, 2.2],
        [73, 199, 1.8],
        [192, 192, 2.2],
        [183, 199, 1.8],
      ],
      white,
      0.85,
    ),
  ),
  mark(
    "Comet blaze",
    "لکه شهاب",
    g(p("M134 85 121 106 124 122 139 99Z", gold, 0), star(126, 122, gold)),
  ),
  mark(
    "Mackerel tabby",
    "راه‌راه ریز",
    shade(
      raw(
        "M95 80 101 99 106 102 105 78Z M114 75 117 103 122 106 123 73Z M133 73 134 106 139 103 142 75Z M151 78 150 102 155 99 161 80Z M41 182 63 187 43 192Z M215 182 193 187 213 192Z",
      ),
    ),
  ),
  mark(
    "Cream cheeks",
    "لپ خامه‌ای",
    cream(
      raw(
        "M43 172 Q71 179 82 201 L65 214 45 196Z M213 172 Q185 179 174 201 L191 214 211 196Z",
      ),
    ),
  ),
  mark(
    "Patchwork",
    "وصله‌پشمی",
    g(
      cream(raw("M49 75 99 75 113 101 84 115 48 104Z")),
      shade(
        raw(
          "M155 78 199 80 208 106 181 119 149 102Z M85 202 118 206 111 223 79 218Z",
        ),
      ),
    ),
  ),
  mark(
    "Tulip forehead",
    "لاله پیشونی",
    g(
      p(
        "M118 97 123 101 128 91 133 101 138 97 Q140 115 128 115 Q116 115 118 97Z",
        rose,
        0,
      ),
      p("M128 115 v10", "none", 1.5),
    ),
  ),
  mark(
    "Soft eyebrows patch",
    "لکه بالای چشم",
    cream(
      raw(
        "M62 103 Q83 79 106 104 L98 113 81 105 67 113Z M194 103 Q173 79 150 104 L158 113 175 105 189 113Z",
      ),
    ),
  ),
  mark(
    "Wish sparkles",
    "برق آرزوها",
    g(star(128, 98, gold), star(105, 87, white), star(151, 87, white)),
  ),
  mark("Chin heart", "قلب چونه", heart(128, 214, white)),
  mark(
    "Dappled coat",
    "پشم خال‌دار",
    spots([
      [94, 85, 5],
      [114, 79, 3],
      [151, 82, 5],
      [170, 91, 3],
      [51, 168, 4],
      [64, 193, 5],
      [86, 208, 3],
      [205, 168, 4],
      [192, 193, 5],
      [170, 208, 3],
    ]),
  ),
  mark(
    "Rose mask",
    "ماسک گلبهی",
    <g fill={rose} opacity=".38">
      {raw(
        "M51 91 Q84 73 111 108 L128 128 145 108 Q172 73 205 91 L210 154 184 170 143 151 128 143 113 151 72 170 46 154Z",
      )}
    </g>,
  ),
  mark(
    "Split blaze",
    "لکه دوشاخه",
    cream(
      raw(
        "M116 74 125 99 128 118 131 99 140 74 151 80 137 117 133 151 143 178 128 189 113 178 123 151 119 117 105 80Z",
      ),
    ),
  ),
  mark(
    "Crescent cheeks",
    "هلال روی لپ",
    g(
      p(
        "M65 184 Q49 194 64 205 Q57 194 72 190Z M191 184 Q207 194 192 205 Q199 194 184 190Z",
        gold,
        0,
      ),
    ),
  ),
  mark(
    "Honey freckles",
    "خال عسلی",
    spots(
      [
        [111, 90, 2],
        [121, 84, 2],
        [134, 87, 2],
        [145, 94, 1.6],
        [65, 191, 2],
        [73, 196, 2],
        [191, 191, 2],
        [183, 196, 2],
      ],
      gold,
      0.85,
    ),
  ),
  mark(
    "Botanical blaze",
    "لکه برگی",
    g(
      cream(raw("M126 80 130 80 131 143 H125Z")),
      p(
        "M128 99 Q111 97 118 85 Q130 87 128 99Z M128 113 Q145 109 139 98 Q128 100 128 113Z",
        mint,
        0,
      ),
    ),
  ),
  mark(
    "Diamond bib",
    "پیش‌بند لوزی",
    cream(
      raw("M89 202 111 194 128 204 145 194 167 202 148 221 128 231 108 221Z"),
    ),
  ),
  mark(
    "Cloud patches",
    "لکه ابری",
    g(
      cream(
        raw("M50 86 Q62 74 73 83 Q86 72 93 87 Q99 100 82 107 Q64 111 52 102Z"),
      ),
      shade(
        raw("M173 195 Q182 181 194 190 Q208 185 213 199 L199 217 172 220Z"),
      ),
    ),
  ),
  mark(
    "Little crown",
    "تاج کوچولو",
    p("M115 95 121 102 128 89 135 102 141 95 137 114 H119Z", gold, 0),
  ),
  mark(
    "Harlequin",
    "لکه شطرنجی",
    g(
      cream(raw("M42 76 H128 V114 H42Z M128 185 H214 V226 H128Z")),
      shade(raw("M128 76 H214 V114 H128Z M42 185 H128 V226 H42Z")),
    ),
  ),
  mark(
    "Paw forehead",
    "پنجه پیشونی",
    g(
      e(128, 110, 7, 6, gold),
      c(118, 100, 3, gold),
      c(128, 95, 3.5, gold),
      c(138, 100, 3, gold),
    ),
  ),
  mark(
    "Wishy diamond trail",
    "رد نگین ویشی",
    g(
      p("M128 95 137 111 128 126 119 111Z", gold, 0),
      p(
        "M128 80 131 85 128 90 125 85Z M109 100 112 105 109 110 106 105Z M147 100 150 105 147 110 144 105Z",
        gold,
        0,
      ),
    ),
  ),
];
const accessory = (name: string, fa: string, art: ReactNode) =>
  d(name, fa, art);
const ribbon = (x: number, y: number, fill = rose) => (
  <g transform={`translate(${x} ${y})`}>
    {p("M0 0 -15 -10 Q-20 0 -15 10Z M0 0 15 -10 Q20 0 15 10Z", fill, 2)}
    {c(0, 0, 4, fill)}
    {p("M-2 -3 2 3", "none", 1)}
  </g>
);
const flower = (x: number, y: number, fill = rose) => (
  <g transform={`translate(${x} ${y})`}>
    {[0, 72, 144, 216, 288].map((a) => (
      <ellipse
        key={a}
        cx="0"
        cy="-7"
        rx="5"
        ry="8"
        fill={fill}
        stroke={catInk}
        strokeWidth="1.5"
        transform={`rotate(${a})`}
      />
    ))}
    {c(0, 0, 4, gold)}
  </g>
);
const glasses = (left: ReactNode, right: ReactNode, detail?: ReactNode) =>
  g(
    left,
    right,
    p("M121 143 Q128 138 135 143 M49 140 42 136 M207 140 214 136", "none", 2.2),
    detail,
  );
export const accessoryDesigns = [
  accessory(
    "Wishy orbit",
    "مدار ویشی",
    p("M43 77 Q15 95 27 79 L77 40 Q98 25 86 40 L67 54 M40 78 49 72", "none", 3),
  ),
  accessory("Just a cat", "فقط گربه", null),
  accessory("Golden bow tie", "پاپیون طلایی", ribbon(128, 224, gold)),
  accessory(
    "Lilac scarf",
    "شال یاسی",
    g(
      p("M87 214 Q128 232 169 214 L164 230 Q128 243 92 230Z", lilac, 2.4),
      p("M143 227 166 241 154 241 147 247 135 230Z", lilac, 2),
      p("M101 225 151 225", "none", 1.2),
    ),
  ),
  accessory(
    "Moon crown",
    "تاج ماه",
    g(
      p("M105 82 100 61 116 70 128 51 140 70 156 61 151 82Z", gold, 2.5),
      p("M130 62 Q119 69 130 76 Q124 69 135 67Z", white, 0),
    ),
  ),
  accessory("Daisy clip", "گیره بابونه", flower(189, 88, white)),
  accessory(
    "Round spectacles",
    "عینک گرد",
    glasses(
      <ellipse
        cx="85"
        cy="149"
        rx="36"
        ry="39"
        fill="none"
        stroke={catInk}
        strokeWidth="3"
      />,
      <ellipse
        cx="171"
        cy="149"
        rx="36"
        ry="39"
        fill="none"
        stroke={catInk}
        strokeWidth="3"
      />,
    ),
  ),
  accessory(
    "Cozy headphones",
    "هدفون نرم",
    g(
      p("M32 139 Q29 65 80 58 M224 139 Q227 65 176 58", "none", 5),
      p("M29 128 Q20 127 20 138 V157 Q20 168 31 166 L39 162 V133Z", mint, 2.5),
      p(
        "M227 128 Q236 127 236 138 V157 Q236 168 225 166 L217 162 V133Z",
        mint,
        2.5,
      ),
    ),
  ),
  accessory(
    "Little beret",
    "کلاه بره",
    g(
      p("M91 83 Q84 61 111 56 Q140 43 163 66 L172 82Z", rose, 2.5),
      p("M88 83 H174 M130 54 134 44", "none", 3),
      p("M103 66 Q112 58 125 59", "none", 1.2),
    ),
  ),
  accessory(
    "Wish bell",
    "زنگوله آرزو",
    g(
      p("M91 215 Q128 232 165 215", "none", 5),
      p("M122 223 Q121 215 128 215 Q135 215 134 223 L139 232 H117Z", gold, 2),
      p("M120 232 h16", "none", 2),
      c(128, 236, 3, gold),
    ),
  ),
  accessory(
    "Rose ear bow",
    "پاپیون صورتی",
    <g transform="rotate(22 188 71)">{ribbon(188, 71, rose)}</g>,
  ),
  accessory(
    "Star pin",
    "سنجاق ستاره",
    g(p("M172 93 197 80", "none", 3), star(185, 85, gold), c(198, 79, 2, gold)),
  ),
  accessory(
    "Party cone",
    "کلاه تولد",
    g(
      p("M104 83 124 35 153 83Z", lilac, 2.5),
      p("M116 54 135 53 M111 67 143 66", "none", 3),
      c(124, 35, 5, gold),
    ),
  ),
  accessory(
    "Forest sprout",
    "جوانه",
    g(
      p("M128 78 V55", "none", 2.5),
      p("M128 65 Q101 65 110 47 Q128 47 128 65Z", mint, 2),
      p("M128 59 Q134 39 151 46 Q152 63 128 59Z", mint, 2),
    ),
  ),
  accessory(
    "Artist bandana",
    "دستمال هنری",
    g(
      p("M91 215 128 224 165 215 148 238 128 244 108 238Z", rose, 2.3),
      c(118, 229, 2, white),
      c(135, 234, 2, white),
      c(143, 226, 2, white),
    ),
  ),
  accessory(
    "Square glasses",
    "عینک چهارگوش",
    glasses(
      p(
        "M61 112 H108 Q121 112 121 125 V170 Q121 187 105 187 H64 Q49 187 49 170 V125 Q49 112 61 112Z",
        "none",
        3,
      ),
      p(
        "M148 112 H195 Q207 112 207 125 V170 Q207 187 192 187 H151 Q135 187 135 170 V125 Q135 112 148 112Z",
        "none",
        3,
      ),
    ),
  ),
  accessory(
    "Tiny top hat",
    "کلاه شعبده",
    g(
      p("M105 80 101 44 H149 L153 80Z", catInk, 2),
      p("M102 63 H151 V72 H103Z", lilac, 0),
      p("M94 81 H165", "none", 4),
      star(130, 68, gold),
    ),
  ),
  accessory(
    "Moon pendant",
    "گردنبند ماه",
    g(
      p("M91 213 Q128 240 165 213", "none", 2.3),
      p("M131 224 Q115 231 128 244 Q122 232 139 232Z", gold, 1.5),
    ),
  ),
  accessory(
    "Cherry clip",
    "گیره گیلاس",
    g(
      p("M179 91 Q190 81 192 70 Q194 82 202 91", "none", 2),
      c(179, 93, 6, rose),
      c(202, 93, 6, rose),
      p("M192 73 Q180 73 183 65 Q194 64 192 73Z", mint, 1.5),
    ),
  ),
  accessory(
    "Woolly beanie",
    "کلاه بافتنی",
    g(
      p("M92 79 Q92 47 128 48 Q164 47 164 79Z", mint, 2.5),
      p("M91 76 H165 V87 H91Z", mint, 2),
      c(128, 44, 7, white),
      p(
        "M105 56 V75 M117 51 V75 M129 51 V75 M141 52 V75 M153 58 V75",
        "none",
        1,
      ),
    ),
  ),
  accessory(
    "Lucky bow",
    "پاپیون شبدر",
    g(
      ribbon(128, 225, mint),
      p("M128 225 q-8 -7 -3 -9 q5 -2 3 9 q7 -8 9 -3 q2 5 -9 3Z", gold, 0),
    ),
  ),
  accessory(
    "Sunflower",
    "آفتابگردون",
    g(flower(188, 86, gold), c(188, 86, 4, catInk), leaf(187, 104)),
  ),
  accessory(
    "Wizard hat",
    "کلاه جادو",
    g(
      p("M93 83 Q116 55 128 31 Q137 58 164 83Z", lilac, 2.5),
      p("M88 83 H170", "none", 3),
      star(128, 64, gold),
      c(140, 76, 2, gold),
    ),
  ),
  accessory(
    "Pearl necklace",
    "گردنبند مروارید",
    g(
      p("M90 213 Q128 238 166 213", "none", 1.5),
      ...[
        [94, 216],
        [105, 222],
        [116, 226],
        [128, 228],
        [140, 226],
        [151, 222],
        [162, 216],
      ].map(([x, y]) => g(c(x, y, 4, white), c(x - 1, y - 1, 1, gold))),
    ),
  ),
  accessory(
    "Paper boat",
    "کلاه قایقی",
    g(
      p("M88 78 128 45 170 78 158 87 H101Z", white, 2),
      p("M88 78 H170 M128 45 V78 L104 87", "none", 1.5),
    ),
  ),
  accessory(
    "Butterfly clip",
    "گیره پروانه",
    g(
      p(
        "M189 86 Q170 62 172 83 Q170 103 189 90 Q208 101 207 82 Q210 63 189 86Z",
        lilac,
        2,
      ),
      p("M189 82 V94 M188 82 184 77 M190 82 195 77", "none", 1.5),
    ),
  ),
  accessory(
    "Explorer scarf",
    "شال ماجراجو",
    g(
      p("M91 213 Q128 232 165 213 L160 230 Q128 242 96 230Z", gold, 2),
      p("M106 229 96 244 109 239 114 246 121 231Z", gold, 2),
      p("M101 219 157 226", "none", 1.2),
    ),
  ),
  accessory(
    "Heart shades frame",
    "عینک قلبی",
    glasses(
      p(
        "M85 124 Q48 95 48 139 Q46 171 85 190 Q124 171 122 139 Q122 95 85 124Z",
        "none",
        3,
      ),
      p(
        "M171 124 Q134 95 134 139 Q132 171 171 190 Q210 171 208 139 Q208 95 171 124Z",
        "none",
        3,
      ),
    ),
  ),
  accessory(
    "Sleep cap",
    "کلاه خواب",
    g(
      p(
        "M96 83 Q96 49 128 47 Q161 42 177 67 L184 88 169 78 Q148 66 148 82Z",
        lilac,
        2.5,
      ),
      c(184, 89, 6, white),
      p("M103 61 111 62 M115 51 122 53 M145 53 150 59", "none", 1.5),
    ),
  ),
  accessory(
    "Gift ribbon",
    "روبان کادو",
    g(
      ribbon(128, 69, gold),
      p("M122 75 113 91 123 88 128 92 131 76Z", gold, 1.8),
    ),
  ),
  accessory(
    "Bumblebee pin",
    "سنجاق زنبور",
    g(
      e(189, 86, 10, 7, gold),
      p("M185 80 v12 M191 80 v12", "none", 2),
      e(184, 76, 4, 6, white),
      e(193, 76, 4, 6, white),
      c(199, 85, 2, catInk),
    ),
  ),
  accessory(
    "Sailor collar",
    "یقه ملوانی",
    g(
      p(
        "M91 211 128 225 165 211 159 232 143 238 128 230 113 238 97 232Z",
        white,
        2,
      ),
      p("M99 219 113 230 128 224 143 230 157 219", "none", 1.5),
      ribbon(128, 232, lilac),
    ),
  ),
  accessory(
    "Soft earmuffs",
    "گوش‌گیر نرم",
    g(
      p("M26 144 Q26 62 77 59 M230 144 Q230 62 179 59", "none", 4),
      p(
        "M29 128 Q15 125 17 140 Q9 147 18 155 Q16 171 30 165 L39 159 V135Z",
        rose,
        2,
      ),
      p(
        "M227 128 Q241 125 239 140 Q247 147 238 155 Q240 171 226 165 L217 159 V135Z",
        rose,
        2,
      ),
    ),
  ),
  accessory(
    "Flower wreath",
    "حلقه گل",
    g(
      p("M79 81 Q128 54 177 81", "none", 2),
      flower(90, 75, rose),
      flower(114, 67, white),
      flower(140, 67, gold),
      flower(165, 76, lilac),
    ),
  ),
  accessory(
    "Little bandage",
    "چسب زخم کوچولو",
    <g transform="translate(192 98) rotate(-28)">
      {p("M-13 -5 H13 Q17 0 13 5 H-13 Q-17 0 -13 -5Z", "#eac69d", 1.5)}
      {p("M-4 -4 H4 V4 H-4Z", rose, 0)}
      {c(-10, 0, 1, catInk)}
      {c(10, 0, 1, catInk)}
    </g>,
  ),
  accessory(
    "Wing collar",
    "یقه بال‌دار",
    g(
      p(
        "M91 213 124 224 113 238 97 228Z M165 213 132 224 143 238 159 228Z",
        lilac,
        2,
      ),
      p("M124 224 128 231 132 224Z", gold, 1.5),
    ),
  ),
  accessory(
    "Frog hat",
    "کلاه قورباغه",
    g(
      p("M91 81 Q93 58 128 59 Q163 58 165 81Z", mint, 2.3),
      c(109, 58, 8, mint),
      c(147, 58, 8, mint),
      c(109, 57, 4, white),
      c(147, 57, 4, white),
      c(109, 57, 2, catInk),
      c(147, 57, 2, catInk),
      p("M121 73 Q128 78 135 73", "none", 1.5),
    ),
  ),
  accessory(
    "Lightning pin",
    "سنجاق برق",
    p("M194 72 177 93 189 92 181 109 206 84 193 85 203 72Z", gold, 1.5),
  ),
  accessory(
    "Lavender sprig",
    "شاخه اسطوخودوس",
    g(
      p("M179 104 196 73", "none", 2),
      p(
        "M187 89 q-15 0 -8 -9 q10 1 8 9Z M191 82 q13 -2 7 -10 q-9 2 -7 10Z M181 99 q-13 0 -7 -8 q9 1 7 8Z",
        lilac,
        1.2,
      ),
    ),
  ),
  accessory(
    "Mushroom cap",
    "کلاه قارچی",
    g(
      p("M89 77 Q89 40 128 43 Q167 40 167 77Z", rose, 2.3),
      p("M89 77 Q128 91 167 77 Q128 69 89 77Z", white, 2),
      c(110, 61, 6, white),
      c(140, 55, 5, white),
      c(155, 68, 4, white),
    ),
  ),
  accessory(
    "Star medal",
    "مدال ستاره",
    g(
      p("M94 216 117 227 123 223 128 230 133 223 139 227 162 216", "none", 4),
      star(128, 237, gold),
      p("M128 229 v-7", "none", 1.5),
    ),
  ),
  accessory(
    "Straw hat",
    "کلاه حصیری",
    g(
      p("M103 75 108 48 Q128 39 148 48 L153 75Z", gold, 2.3),
      p("M91 78 Q128 64 165 78 Q168 87 128 88 Q88 87 91 78Z", gold, 2),
      p("M104 66 H152 V74 H103Z", rose, 0),
      p("M114 48 111 63 M126 46 V63 M139 47 142 63", "none", 1),
    ),
  ),
  accessory(
    "Tiny crown pin",
    "سنجاق تاج",
    <g transform="translate(190 89) rotate(22)">
      {p("M-12 4 -14 -10 -6 -4 0 -14 6 -4 14 -10 12 4Z", gold, 1.7)}
      {c(0, -3, 2, white)}
    </g>,
  ),
  accessory(
    "Denim neckerchief",
    "دستمال آبی",
    g(
      p("M91 214 128 224 165 214 145 235 128 244 111 235Z", "#8cb6d9", 2.2),
      p("M98 219 128 238 158 219", "none", 1),
      c(128, 231, 2, white),
    ),
  ),
  accessory(
    "Rainbow clip",
    "گیره رنگین‌کمون",
    g(
      p("M175 98 Q185 71 204 91", "none", 7),
      <path
        d="M175 98 Q185 71 204 91"
        fill="none"
        stroke={rose}
        strokeWidth="5"
      />,
      <path
        d="M178 99 Q187 79 201 93"
        fill="none"
        stroke={gold}
        strokeWidth="3"
      />,
      c(175, 99, 4, white),
      c(203, 94, 4, white),
    ),
  ),
  accessory(
    "Space antenna",
    "آنتن فضایی",
    g(
      p("M128 77 V55 Q139 48 135 39", "none", 2.5),
      c(134, 36, 6, mint),
      star(134, 36, white),
    ),
  ),
  accessory(
    "Heart pendant",
    "گردنبند قلب",
    g(
      p("M92 213 Q128 238 164 213", "none", 2),
      <g transform="translate(128 234)">{heart(0, 0, rose)}</g>,
      c(125, 229, 1.5, white),
    ),
  ),
  accessory(
    "Little feather",
    "پر کوچولو",
    g(
      p(
        "M180 106 Q198 92 202 66 Q183 66 180 87 L186 83 180 94 187 90Z",
        mint,
        1.8,
      ),
      p("M182 99 197 73", "none", 1.2),
    ),
  ),
  accessory(
    "Gift box hat",
    "کلاه جعبه کادو",
    g(
      p("M104 49 H152 V80 H104Z", lilac, 2),
      p("M101 49 H155 V58 H101Z", lilac, 2),
      p("M124 49 H132 V80 H124Z", gold, 0),
      ribbon(128, 46, gold),
    ),
  ),
  accessory(
    "Wishy neck gem",
    "گردنبند نگین ویشی",
    g(
      p("M92 214 Q128 237 164 214", "none", 3),
      p("M128 221 138 232 128 245 118 232Z", gold, 1.8),
      p("M128 225 133 232 128 240 123 232Z", "#ffe28a", 0),
    ),
  ),
];

export const catArtwork = {
  face: faceDesigns,
  ears: earDesigns,
  eyes: eyeDesigns.map(({ name, fa }, value) =>
    d(name, fa, <EyeShapes value={value} />),
  ),
  pupils: pupilDesigns,
  brows: browDesigns,
  nose: noseDesigns,
  mouth: mouthDesigns,
  whiskers: whiskerDesigns,
  markings: markingDesigns,
  accessories: accessoryDesigns,
};
