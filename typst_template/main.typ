#import "template.typ": *

// Take a look at the file `template.typ` in the file panel
// to customize this template and discover how it works.
#show: project.with(
  title: "Pandion Labs",
  logo: "logo.png",
  doc_number: "", //maybe we can auto generate a doc numbering system one day
  authors: (
    (name: "Sam Herniman", email: "sam@pandionlabs.dev"),
    (name: "Simone Massaro", email: "simone@pandionlabs.dev"),
    (name: "Anna Dodd", email: "anna@pandionlabs.dev"),
  ),
  date: "10 June 2025",
)

// We generated the example code below so you can see how
// your document will look. Go ahead and replace it with
// your own content!

= Introduction
#lorem(60)

== In this paper
#lorem(20)

=== Contributions
#lorem(40)

= Related Work
#lorem(500)

