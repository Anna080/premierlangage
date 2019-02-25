import { Resource } from './resource.model';
import { IEditorTab } from '../services/core/opener.service';

export const DISALLOWED_CHAR = ['/', ' ', '\t', '\n', ';', '#', '+', '&'];

export function canRead(item: Resource) {
    return item && item.read;
}

export function canWrite(item: Resource) {
    return item &&  item.write;
}

export function readonly(item: Resource) {
    return !canWrite(item);
}

export function isFolder(item: Resource) {
    return item &&  item.type === 'folder';
}

export function isFile(item: Resource) {
    return item &&  item.type === 'file';
}

export function isRoot(item: Resource) {
    return item &&  item.name === 'home' || item.name === 'home/'
    || item.name === 'lib' || item.name === 'lib/';
}

export function isPl(item: Resource) {
    return item &&  item.name.endsWith('.pl');
}

export function isMarkdown(item: Resource) {
    return item &&  item.name.endsWith('.md');
}

export function isPltp(item: Resource) {
    return item &&  item.name.endsWith('.pltp');
}

export function canBePreviewed(item: Resource) {
    return item && isPl(item) || isSVG(item);
}

export function isHome(item: Resource) {
    return item && item.name === 'home';
}

export function isNotRoot(item: Resource) {
    return !isRoot(item);
}

export function isSVG(item: Resource) {
    return extension(item) === 'svg';
}

export function fromServer(resource: Resource) {
    return !resource.meta || resource.meta.download_url;
}

export function isRepo(item: Resource) {
    return item && item.repo;
}

export function canAddFile(item: Resource) {
    return canWrite(item) && isFolder(item);
}

export function canCopy(item: Resource) {
    return canRead(item) && isNotRoot(item);
}

export function canAddFolder(item: Resource) {
    return canWrite(item) && isFolder(item);
}

export function canBeRenamed(item: Resource) {
    return canWrite(item) && !isRoot(item);
}

export function canBeDeleted(item: Resource) {
    return canWrite(item) && isNotRoot(item);
}

export function canBeTested(item: Resource) {
    return canRead(item) && isPl(item);
}

export function canBeLoaded(item: Resource) {
    return canWrite(item) && isPltp(item);
}

export function canBeReloaded(item: Resource) {
    return canWrite(item) && isPltp(item);
}

export function extension(resource: Resource) {
    const dotIndex = resource.name.lastIndexOf('.');
    return resource.name.substring(dotIndex + 1);
}

export function canBeUsedAsFileName(name: string) {
    return name && DISALLOWED_CHAR.every(e => !name.includes(e));
}

export function checkName(name: string) {
    if (!canBeUsedAsFileName(name)) {
        throw new Error(name + ' cannot sould not contains any of ' + DISALLOWED_CHAR);
    }
}

export function requireNonNull(param: any, name: string) {
    if  (!param && typeof(param) !== 'boolean') {
        throw new TypeError(name + ' param is required !');
    }
}

export function assert(condition: any, message: string) {
    if  (!condition) {
        throw new Error(message);
    }
}

export function basename(path: string) {
    if (!path) {
        return path;
    }
    const array = path.split('/');
    return array[array.length - 1];
}

export function asURI(resource: Resource) {
    const monaco = (<any>window).monaco;
    return monaco.Uri.file(resource.path);
}

export function asTab(resource: Resource, preview?: boolean): IEditorTab {
    return {
        resource: resource,
        uri: asURI(resource),
        title: preview ? 'Preview \'' + resource.name + '\'' : resource.name,
        preview: preview,
        icon: resource.icon
    };
}

export function compareTab(tab1: IEditorTab, tab2: IEditorTab) {
    return tab1.resource.path === tab2.resource.path;
}


export function resourceIsURI(resource: Resource, uri: monaco.Uri) {
    return '/' + resource.path === uri.path;
}

export function openAsCode(data: IEditorTab) {
    return !openAsImage(data);
}

export function openAsImage(data: IEditorTab) {
    return !openAsPreview(data) && data.resource.meta && data.resource.meta.image && !isSVG(data.resource);
}

export function openAsPreview(data: IEditorTab) {
    return data.resource.meta && data.resource.meta.html !== undefined;
}
