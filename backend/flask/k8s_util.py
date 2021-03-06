"""
Util class for k8s access
"""
from kubernetes import client

import const


def make_job_spec(**kwargs):
  """
k8s job spec 을 생성합니다.

:param: learning_rate, epoch, experiment_id
:return: V1Job
:rtype: V1Job
"""
  job = client.V1Job()
  # label
  label = dict()
  label['mlmodel'] = 'ae'
  job.metadata = client.V1ObjectMeta(name="ae",  # 이름 겹치지 않게 generator 사용
                                     labels=label)

  # volumes
  in_volume = client.V1Volume(name='in-storage',
                              persistent_volume_claim=
                              client.V1PersistentVolumeClaimVolumeSource(
                                claim_name='pvc-input'))
  out_volume = client.V1Volume(name='out-storage',
                               persistent_volume_claim=
                               client.V1PersistentVolumeClaimVolumeSource(
                                 claim_name='pvc-output'))

  # volumeMount
  in_volume_mount = client.V1VolumeMount(mount_path=const.INPUT_MOUNT_PATH,
                                         name='in-storage')
  out_volume_mount = client.V1VolumeMount(mount_path=const.OUTPUT_MOUNT_PATH,
                                          name='out-storage')

  # envs
  env_lr = client.V1EnvVar(name='LEARNING_RATE', value=kwargs.get('lr'))
  env_epoch = client.V1EnvVar(name='EPOCH', value=kwargs.get('epoch'))
  env_ex_id = client.V1EnvVar(name='EXPERIMENT_ID', value=kwargs.get('ex_id'))
  env_output_path = client.V1EnvVar(name='OUTPUT_MOUNT_POINT',
                                    value=const.OUTPUT_MOUNT_PATH)
  envs = [env_lr, env_epoch, env_ex_id, env_output_path]

  # container
  container = client.V1Container(name=const.AE_MODEL_NAME,
                                 image=const.AE_MODEL_IMAGE_URL,
                                 # TODO image tag 는 parameter 로 제공, DB 관리
                                 image_pull_policy='Always',
                                 volume_mounts=[in_volume_mount,
                                                out_volume_mount],
                                 env=envs)

  # pod spec
  pod_spec = client.V1PodSpec(service_account_name=const.SERVICE_ACCOUNT_NAME,
                              restart_policy='OnFailure',
                              containers=[container],
                              volumes=[in_volume, out_volume])
  template = client.V1PodTemplateSpec(spec=pod_spec)

  # job spec
  spec = client.V1JobSpec(template=template, backoff_limit=3)
  job.spec = spec

  return job
