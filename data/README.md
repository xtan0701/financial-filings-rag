# Filing snapshots

The PDFs are the input snapshots supplied with this project. They are third-party company disclosures, not authored datasets. No new download or transformation was used to prepare these copies.

| Snapshot | Fiscal year end | PDF pages | Format notes |
| --- | --- | --- | --- |
| [Alphabet](filings/alphabet-2024-10k.pdf) | 2024-12-31 | 99 | PDF filing |
| [Amazon](filings/amazon-2024-10k.pdf) | 2024-12-31 | 89 | PDF filing |
| [Microsoft](filings/microsoft-2024-10k.pdf) | 2024-06-30 | 221 | Printed filing with browser headers and footers |

The [manifest](manifest.csv) stores relative filename, company, fiscal year end, physical PDF page count, byte length, and SHA-256. The snapshots are byte-identical to the supplied local PDFs. Acquisition dates for Alphabet and Amazon were not recorded; Microsoft's rendered footer includes a March 4, 2025 print timestamp. These are snapshot observations, not verified download records.

## Units and interpretation

There is no normalized financial table in this project. Amounts, currency, scale, fiscal period, and accounting scope must be read from each filing's table heading or footnote. Do not assume all amounts have the same units or that the three fiscal years cover identical dates.

`PyPDFLoader` extracts page text. The splitter measures characters. It does not perform table reconstruction, OCR, currency conversion, or accounting-period alignment. Repeated headers, line breaks, and text ordering can affect retrieval.

For authoritative filings or replacement documents, use the companies' investor relations sites or the [SEC EDGAR company search](https://www.sec.gov/edgar/search/). Replacement bytes may change extraction, pagination, and model responses; update the manifest if replacing a snapshot.

The unrelated paper and resume examples from the setup package are outside this financial corpus and are not distributed here.
