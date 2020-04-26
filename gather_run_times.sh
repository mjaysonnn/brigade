#!/bin/bash
kubectl get pods -o=jsonpath="{range .items[*]}\
{.metadata.name}{','}\
{.metadata.uid}{','}\
{.metadata.creationTimestamp}{','}\
{'statusConditionsBegin'}{','}\
{.status.conditions[0].type}{','}\
{.status.conditions[0].lastTransitionTime}{','}\
{.status.conditions[0].status}{','}\
{.status.conditions[1].type}{','}\
{.status.conditions[1].lastTransitionTime}{','}\
{.status.conditions[1].status}{','}\
{.status.conditions[2].type}{','}\
{.status.conditions[2].lastTransitionTime}{','}\
{.status.conditions[2].status}{','}\
{.status.conditions[3].type}{','}\
{.status.conditions[3].lastTransitionTime}{','}\
{.status.conditions[3].status}{','}\
{'statusConditionsEnd'}{','}\
{.status.containerStatuses[].state.terminated.startedAt}{','}\
{.status.containerStatuses[].state.terminated.finishedAt}{','}\
{.status.initContainerStatuses[].state.terminated.finishedAt}{','}\
{.status.initContainerStatuses[].state.terminated.startedAt}{','}\
{.status.startTime}{','}\
{.spec.containers[0].imagePullPolicy}{','}\
{'\n'}{end}" > pod_logs/all_pods_output.csv
