// The project function defines how your document looks.
// It takes your content and some metadata and formats it.
// Go ahead and customize it to your liking!
#let project(
  title: "",
  authors: (),
  date: none,
  logo: none,
  doc_number: none,
  body,
) = {
  // Set the document's basic properties.
  set document(author: authors.map(a => a.name), title: title)
  set page(
    numbering: "1", 
    number-align: center
  )

  // Save heading and body font families in variables.
  let body-font = "Libertinus Serif"
  let sans-font = "Atkinson Hyperlegible Next"

  // Set body font family.
  set text(font: body-font, lang: "en")
  show heading: set text(font: sans-font)
  set heading(numbering: "1.a")

  // Set run-in subheadings, starting at level 3.
  show heading: it => {
    if it.level > 2 {
      parbreak()
      text(11pt, style: "italic", weight: "regular", it.body + ".")
    } else {
      it
    }
  }


  // Title page.
  // The page can contain a logo if you pass one with `logo: "logo.png"`.
  v(0.6fr)
  if logo != none {
    align(right, link("https://pandionlabs.dev/", image(logo, width: 30%)))
  }
  v(9.6fr)

  text(1.1em, date)
  h(1.2em, weak: true)
  text(1.1em, doc_number)
  v(1.2em, weak: true)
  text(font: sans-font, 2em, weight: 700, title)

  // Author information.
  pad(
    top: 0.7em,
    right: 20%,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1em,
      ..authors.map(author => align(start)[
        *#author.name* \
        #author.email
      ]),
    ),
  )

  v(2.4fr)
  pagebreak()


  // Main body.
  set par(justify: true)
  set page(header: [
    #set text(font: sans-font, lang: "en")
    #date 
    #h(0.6em, weak: true)
    #doc_number
    #h(1fr)
    Pandion Labs
      //#image("logo.png")
    #rect(
      width: 100%,
      height: 1.5pt,
      fill: gradient.linear(
        rgb("#71fdbf"), rgb("#fed273")
      ),
      radius: 1.5pt
)

    ]
  )
  body
}