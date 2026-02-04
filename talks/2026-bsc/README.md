## Worflow


```mermaid
flowchart TD
  subgraph IRAMAT[<b>IRAMAT</b>]
  	ICP{{ICP-MS}}
  	XRD{{XRD}}
	XRF{{XRF}}
    BD[(DB)]
    analyses[archaeometry analysis]
    analyses --> IRAMATdata
    analyses --> IRAMATimg
	subgraph VM[VM]
    subgraph IRAMATdata[Scalar measurements]
		XRF --> BD
		XRD --> BD
		ICP --> BD
        BD -- API RESTful --> APIdata[<em>labeled data</em>]
    end
    subgraph IRAMATimg[Imaging]
        Macro{{Macro-<br>photography}} -- format --> IIIFimg([IIIF image])
        Opt{{Optical<br>Microscopy}} -- format --> IIIFimg
        SEM{{SEM-EDS}} -- format --> IIIFimg
        Raman{{Raman}} -- format --> IIIFimg
        IIIFimg ---> IIIFpres([IIIF presentation])
		IIIFpres --> IIIFannot([IIIF annotation])
		IIIFannot -- manifests<br>annotations --> BD
        BD -- API RESTful --> APIimg[<em>labeled images</em>]
    end
	end
  end
  APIdata ---> PyExtract[<em>Data Fusion</em>]
  APIimg ---> PyExtract
  subgraph BSC[<b>BSC</b>]
    PyExtract -- creates --> MLlearn[(learning base)]
    subgraph ML[Machine Learning]
      MLlearn ---> MLvalid[validation]
      MLvalid ---> MLtest[test]
      MLtest --> MLlearn
    end
  end
    subgraph out[<b>Automatic Classification</b>]
      ResMet[archaeometallurgical facies]
      ResNum[numismatic coins]
    end
  ML ---> out

style BD fill:#cccccc

style IRAMAT fill:#edfa05
style VM fill:#f4fa82
style analyses fill:#fbfcd7
style IRAMATdata fill:#fbfcd7
style IRAMATimg fill:#fbfcd7
style XRF fill:#f6f7d5
style XRD fill:#f6f7d5
style ICP fill:#f6f7d5
style Macro fill:#f6f7d5
style Opt fill:#f6f7d5
style SEM fill:#f6f7d5
style Raman fill:#f6f7d5
style IIIFimg fill:#f6f7d5
style IIIFpres fill:#f6f7d5
style IIIFannot fill:#f6f7d5
style BD fill:#c9c9c9
style APIdata fill:#f6f7d5
style APIimg fill:#f6f7d5

style BSC fill:#4256fc
style PyExtract fill:#8794ff
style ML fill:#8794ff
style MLlearn fill:#d9ddff
style MLvalid fill:#d9ddff
style MLtest fill:#d9ddff

style out fill:#42ff70
style ResMet fill:#b0ffc3
style ResNum fill:#b0ffc3

click BD "https://github.com/iramat/iramat-dev/main/talks/2026-bsc/README.md#db"
click VM "https://github.com/iramat/iramat-dev/main/talks/2026-bsc/README.md#vm"
click IIIFimg "https://github.com/iramat/iramat-dev/main/talks/2026-bsc/README.md#iiif-image"
click IIIFpres "https://github.com/iramat/iramat-dev/main/talks/2026-bsc/README.md#iiif-presentation"
click IIIFannot "https://github.com/iramat/iramat-dev/main/talks/2026-bsc/README.md#iiif-annotation"
```


## Examples

### VM

Ubuntu 22.04 LTS Virtual Machine, hosted by the [Université of Paris-Saclay Mésocentre](https://mesocentre.universite-paris-saclay.fr/)

### DB

- [CHIPS (Chimie en PaléoSidérurgie) Database](https://iramat-apps.cnrs.fr/dash/)

### IIIF

#### IIIF image

- [info.json example](https://iramat-apps.cnrs.fr/iiif/2/acies%2FSeax_sample_process.tif/info.json)
- [Cantaloupe example](https://iramat-apps.cnrs.fr/iiif/2/acies%2FSeax_sample_process.tif/full/full/0/default.jpg)

#### IIIF presentation

- [Manifest example](https://iramat-apps.cnrs.fr/iiif/manifest_seax.json)
- ~~[Mirador image example](https://iramat-apps.cnrs.fr/page/puddled.html)~~
- [Mirador image example](https://jpadfield.github.io/simple-mirador/Standard_Example.html)

#### IIIF annotation

- [TODO]()