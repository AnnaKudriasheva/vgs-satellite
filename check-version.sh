#!/bin/sh

VERSION=$(node -pe "require('./package.json').version")
if [ "${VERSION}" != "${CIRCLE_TAG}" ]; then
    echo "The app version (${VERSION}) does not match GIT tag (${CIRCLE_TAG})." >&2
    exit 1
fi
