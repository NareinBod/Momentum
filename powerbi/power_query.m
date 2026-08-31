// Change SourceFolder to the absolute path of this repository's data\processed directory.
let
    SourceFolder = "C:\\Momentum\\data\\processed\\",
    LoadCsv = (FileName as text) as table =>
        let
            Source = Csv.Document(File.Contents(SourceFolder & FileName), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
            Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true])
        in Headers
in
    LoadCsv
