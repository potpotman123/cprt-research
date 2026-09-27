# Alternative-parts sourcing pilot — 26 September 2026

## Finding
The available retail snapshots do not identify a stable SUV parts premium. Holding the two components constant, the sign differs across retailers. This is a failed robustness check for calibrating a single premium, but a useful reason to model sourcing explicitly. It does not establish a causal sourcing effect: vendors, snapshot vintages and finish certainty differ.

## Reproducible comparison
One left front fender plus one hood; no insulation, labor, paint, freight, tax or other repair operations. Same seller within each row; OEM and aftermarket rows use different sellers. OE numbers on aftermarket listings are fitment cross-references, not evidence the products are genuine Toyota. CAPA status is retailer-reported, not independently audited.

| Price source | Camry | RAV4 | RAV4 / Camry − 1 |
|---|---:|---:|---:|
| OEM dealer | $724.10 | $718.53 | -0.77% |
| PaintedAutoParts | $319.70 | $396.20 | +23.93% |
| CarParts | $333.48 | $306.98 | -7.95% |

CarParts has clearer finish comparability (steel, primed), but its Camry hood snapshot is reported as 11 months old. PaintedAutoParts has an unresolved base-price/painting-option issue and a two-month-old Camry hood snapshot. These are diagnostic scenarios, not current purchasable baskets. Add-to-cart text is not independent inventory confirmation.

## Historical frequency sensitivity
Using the previously documented pooled 2015 Mitchell fender and hood weights (0.2183 and 0.1344) gives the following partial indices. These weights are neither current nor body-specific, and one component per replacement is assumed. This exercise is a robustness diagnostic, not expected total repair cost.
- OEM dealer: Camry 115.1746, RAV4 119.7805; difference +4.00%.
- PaintedAutoParts: Camry 48.7400, RAV4 62.7778; difference +28.80%.
- CarParts: Camry 50.8597, RAV4 46.8366; difference -7.91%.

## Source ledger
Prices are USD public display prices retrieved through web page extraction. A reported crawl age is metadata, not proof of a transaction date. Earlier search snippets sometimes differed from opened pages; opened-page prices supersede them for this calculation. No OCR, paid data or large scrape was used.

- **PaintedAutoParts Camry fender**: $68.80; SKU BG009240; OE reference 5381206210; reported crawl age today. [Listing](https://paintedautoparts.com/toyota-camry-fender-left-capa-oem-5381206210-2015-2017.html). Seller CAPA label; displayed base-price finish not conclusively resolved; painting selector and inconsistent marketing text. Provisional only.
- **PaintedAutoParts RAV4 fender**: $113.57; SKU BG009379; OE reference 538020R050; reported crawl age today. [Listing](https://paintedautoparts.com/toyota-rav4-fender-left-capa-oem-538020r050-2013-2018.html). Seller CAPA label; displayed base-price finish not conclusively resolved; painting selector and inconsistent marketing text. Provisional only.
- **PaintedAutoParts Camry hood**: $250.90; SKU BG036560; OE reference 5330106160; reported crawl age 2 months. [Listing](https://paintedautoparts.com/toyota-camry-hood-capa-oem-5330106160-2015-2017.html). Seller CAPA label; displayed base-price finish not conclusively resolved; painting selector and inconsistent marketing text. Provisional only.
- **PaintedAutoParts RAV4 hood**: $282.63; SKU BG036614; OE reference 533010R050; reported crawl age today. [Listing](https://paintedautoparts.com/toyota-rav4-hood-capa-oem-533010r050-2013-2018.html). Seller CAPA label; displayed base-price finish not conclusively resolved; painting selector and inconsistent marketing text. Provisional only.
- **CarParts Camry fender**: $71.99; SKU REPT220198Q; OE reference 5381206210; reported crawl age today. [Listing](https://www.carparts.com/details/fender/replacement/rept220198q). Seller CAPA label, steel primed. Camry hood price from older 2016 fitment page for shared part; not a simultaneous current quote. No VIN/checkout validation.
- **CarParts RAV4 fender**: $66.49; SKU REPT220180Q; OE reference 538020R050 / 5380242200; reported crawl age today. [Listing](https://www.carparts.com/details/fender/replacement/rept220180q). Seller CAPA label, steel primed. Camry hood price from older 2016 fitment page for shared part; not a simultaneous current quote. No VIN/checkout validation.
- **CarParts Camry hood**: $261.49; SKU REPT130124Q; OE reference 5330106160; reported crawl age 11 months. [Listing](https://www.carparts.com/details/Toyota/Camry/Replacement/Hood/2016/REPT130124Q.html). Seller CAPA label, steel primed. Camry hood price from older 2016 fitment page for shared part; not a simultaneous current quote. No VIN/checkout validation.
- **CarParts RAV4 hood**: $240.49; SKU REPT130118Q; OE reference 533010R050; reported crawl age today. [Listing](https://www.carparts.com/details/hood/replacement/rept130118q). Seller CAPA label, steel primed. Camry hood price from older 2016 fitment page for shared part; not a simultaneous current quote. No VIN/checkout validation.

OEM observations and their source URLs are preserved in `matched_parts_results.json`. Earlier snippets included a CarParts RAV4 fender at $85.99 versus $66.49 on the opened page, and PaintedAutoParts RAV4 fender at $78.98 versus $113.57 on the opened page. These discrepancies warn against treating the apparent precision as economic certainty.

## Recycled-parts outcome
No complete matched recycled basket was established in this bounded search. A sold damaged Camry hood was excluded. Other listings required quotes or had no unambiguous public sale price. Recycled prices remain missing, not zero and not an assumed percentage discount. The JSON records rejected source URLs.

## Mechanism and model treatment
For each vehicle age/body group and component, expected parts expense requires replacement incidence × quantity × the sourcing-share-weighted price. OEM, aftermarket and recycled shares may differ by both component and vehicle; equal shares across body groups cannot be assumed. Add labor, paint and other operations separately. Repairability decisions also require vehicle cash value and salvage recovery, so even a valid parts index does not by itself identify total-loss frequency.

A vehicle can have a more expensive OEM component yet a cheaper substitute at a particular retailer. Consequently, an OEM-only comparison can misstate relative repair costs when actual repairs use alternatives. This pilot documents that vulnerability; it does not measure how insurers source parts, nor prove the market-average direction.

The small pair and availability-selected components cannot support the earlier 1% whole-repair assumption or establish a replacement estimate. Do not compare these panel-only ratios directly against the model’s approximately 18% whole-repair break-even threshold. No CPRT forecasts have been changed.

## Cheapest useful next validation
Before expanding vehicles or parts, obtain simultaneous delivered-price quotes for these same four SKUs with identical finish specifications, then matched itemized estimates to observe sourcing and labor. Public quotes can validate the price comparison; they cannot identify sourcing frequencies. If public data cannot support the latter, preserve explicit scenario ranges instead of fitting a point estimate. More generic catalog searching has diminishing value at this stage.
