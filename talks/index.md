---
marp: true
theme: default
paginate: true
style: |
  section {
    background: #fff;
  }
h1, h2, h3 {
  color: #2b3a42;
}
---
  
  <!-- _class: lead -->
  
  # 🧭 Open Source Explorer
  ### A Zooming Presentation Template for Collaborative Knowledge Sharing
  
  ---
  
  ## 🛠️ Project Overview
  
  - Built with **Marp** & **Markdown**
  - Hosted on **GitHub Pages**
  - Collaborators contribute via **pull requests**
  
  ---
  
  ## 🌱 Section: Introduction to Open Source
  
  - What is Open Source?
  - Licenses (MIT, GPL, CC)
- Community Contributions

---
  
  ## 🔍 Section: Use Case - Data Visualization Tools
  
  - **Dash**
  - **Plotly**
  - **Leaflet** / **Folium**
  - **QGIS**
  
  ---
  
  ## 🚀 Section: How to Contribute
  
  - Clone or fork the repository
- Edit or add a new section (using `---`)
- Submit a pull request

```bash
# Example:
---
  ## 🎨 New Section: Visual Design Tools
  - Figma
- Inkscape
- Krita
---
  ```

---
  
  ## 🔗 Navigation Tips (Zoom effect)
  
  You can simulate **zoom** by nesting content or using linkable sections:
  
  ```md
[Go to Visualization Section](#section-use-case-data-visualization-tools)
  ```
  
  Also supported:
    - [Marp advanced features](https://marpit.marp.app/markdown)
  - Embedded HTML/CSS/JS
  
  ---
    
    ## 📦 Deployment (GitHub Pages)
    
    ```yaml
  # .github/workflows/deploy.yml
  name: Deploy Marp Slide
  on: [push]
  jobs:
    build:
    runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v2
  - name: Convert to HTML
  run: npx @marp-team/marp-cli@latest slides.md -o docs/index.html
  - name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
  publish_dir: ./docs
  ```
  
  ---
    
    ## 🎉 Let’s Build This Together
    
    Feel free to [open issues](https://github.com/your-org/your-repo/issues) or start editing!
    
    - Designed for community projects
  - Easily maintainable & extendable
  
  ---
    
    ## ✨ Thank you!
    
    Contribute, fork, and remix!
    
    > [https://github.com/your-org/zoom-presentation](https://github.com/your-org/zoom-presentation)
  