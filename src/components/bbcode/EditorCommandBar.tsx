import * as React from 'react';

import { ITextEditorHandle } from './TextEditor';

interface ICommandBarProps {
    isPreview: boolean;
    toggleMode: () => void;
    getHandle: () => ITextEditorHandle;
    commitContent: (content: string) => void;
}

export default function CommandBar(props: ICommandBarProps) {
    let primary = buildCommands([
        getModeCommand(props)
    ]);
    let secondary = getSecondaryCommandSet(props);
    return (
        <div style={{ display: 'flex', 'margin-bottom': '4px' }}>
            <div className="btn-toolbar" style={{ 'margin-right': '20px' }}>
                {primary}
            </div>
            {secondary}
        </div >
    );
}

function FontIcon(props: { type: string }) {
    let className = `fa fa-${props.type}`;
    return <i className={className} style={{ 'font-size': '14px' }} />;
}

interface ICommandProps {
    icon?: string;
    label?: string;
    tooltip?: string;
    onExecute: () => void;
}
function Command(props: ICommandProps) {
    return <button type="button" className="btn btn-sm btn-default" title={props.tooltip} onClick={props.onExecute}>
        {props.icon && <FontIcon type={props.icon} />}
        {props.label}
    </button>;
}

function getModeCommand(props: ICommandBarProps): ICommandProps {
    if (!props.isPreview) {
        return {
            label: 'Preview',
            tooltip: 'Switch to preview mode',
            onExecute: () => {
                const handle = props.getHandle();
                if (handle) {
                    props.commitContent(handle.getContent());
                    props.toggleMode();
                }
            }
        };
    }

    return {
        label: 'Edit',
        tooltip: 'Switch to edit mode',
        onExecute: () => { props.toggleMode(); }
    };
}

function buildCommands(commands: ICommandProps[]) {
    return commands.map((props: ICommandProps) => {
        return React.createElement(Command, props);
    });
}

function getSecondaryCommandSet(props: ICommandBarProps) {
    if (props.isPreview) {
        return;
    }

    const injectTag = (tag: string, value?: string) => {
        return () => {
            const handle = props.getHandle();
            if (handle) {
                handle.injectTag(tag, value);
            }
        };
    };

    let commands: ICommandProps[] = [
        {
            icon: 'bold',
            tooltip: 'Bold',
            onExecute: injectTag('b')
        }, {
            icon: 'italic',
            tooltip: 'Italic',
            onExecute: injectTag('i')
        }, {
            icon: 'underline',
            tooltip: 'Underline',
            onExecute: injectTag('u')
        }, {
            icon: 'strikethrough',
            tooltip: 'Strikethrough',
            onExecute: injectTag('s')
        }, {
            icon: 'link',
            tooltip: 'Link',
            onExecute: injectTag('url', 'https://example.com')
        }, {
            icon: 'image',
            tooltip: 'Image',
            onExecute: injectTag('img')
        }, {
            icon: 'eye-slash',
            tooltip: 'Hide',
            onExecute: injectTag('hide')
        }, {
            icon: 'quote-left',
            tooltip: 'Quote',
            onExecute: injectTag('quote')
        }, {
            icon: 'text-height',
            tooltip: 'Text size in pixels',
            onExecute: injectTag('size', '12')
        }, {
            icon: 'paint-brush',
            tooltip: 'Text color',
            onExecute: injectTag('color', '#000000')
        }, {
            icon: 'align-center',
            tooltip: 'Align center',
            onExecute: injectTag('align', 'center')
        }, {
            icon: 'align-right',
            tooltip: 'Align right',
            onExecute: injectTag('align', 'right')
        }, {
            icon: 'code',
            tooltip: 'Code',
            onExecute: injectTag('code')
        }, {
            icon: 'list',
            tooltip: 'List',
            onExecute: injectTag('*')
        }, {
            icon: 'info',
            tooltip: 'BBCode help',
            onExecute: () => {
                console.log('Go to help page');
            }
        }
    ];
    return (
        <div className="btn-toolbar">
            {buildCommands(commands)}
        </div>
    );
}