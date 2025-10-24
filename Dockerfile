# Build site
FROM python:3.12-slim AS build
WORKDIR /site
COPY scripts/requirements.txt /site/scripts/requirements.txt
RUN pip install --no-cache-dir -r scripts/requirements.txt mkdocs-material mkdocs-awesome-pages-plugin mkdocs-section-index mkdocs-glightbox mkdocs-git-revision-date-localized-plugin
COPY . /site
RUN python scripts/build_indexes.py && mkdocs build --strict --site-dir /out

# Serve static
FROM nginx:stable
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /out /usr/share/nginx/html
EXPOSE 80
