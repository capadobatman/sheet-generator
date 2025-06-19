# Random Score Generator

A web-based tool for generating random musical scores using Python, Flask, music21, and LilyPond. A new score is created with a single click and rendered as an image in the browser.

## Features

- Random score generation 
- LilyPond rendering to `.png`
- Flask web interface
- Light/dark mode toggle (built-in)
- Works locally or via Docker

---

## Run with Docker (Recommended)

**No need to install Python or LilyPond on your system.**

### Requirements:
- [Docker](https://www.docker.com/)

### Steps:

```bash
git clone https://github.com/capadobatman/sheet-generator.git
cd sheet-generator
docker-compose up --build
