using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System;
using uPLibrary.Networking.M2Mqtt;
using uPLibrary.Networking.M2Mqtt.Messages;
using uPLibrary.Networking.M2Mqtt.Utility;
using uPLibrary.Networking.M2Mqtt.Exceptions;

public class animController : MonoBehaviour
{
    Animator anim;
    string msg;
    MqttClient client;
    List<String> triggers = new List<string>();


    // Use this for initialization
    void Start()
    {
        anim = gameObject.GetComponentInChildren<Animator>();
        triggers.Add("play_fechar");
        triggers.Add("play_abrir");
        triggers.Add("play_flexao");
        triggers.Add("play_extensao");
        triggers.Add("play_supinacao");
        triggers.Add("play_pronacao");

        client = new MqttClient("127.0.0.1");
        client.MqttMsgPublishReceived += OnMqttMsgReceived;

        string clientId = Guid.NewGuid().ToString();
        client.Connect(clientId);

        client.Subscribe(new string[] { "move" },
        new byte[] {
            MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE }
        );

    }

    void OnMqttMsgReceived(object sender, MqttMsgPublishEventArgs e)
    {
        var topic = e.Topic;

        if (topic == "move")
        {
            msg = System.Text.Encoding.UTF8.GetString(e.Message);
        }
    }

    // Update is called once per frame
    void Update()
    {
        switch (msg)
        {
            case "fecha":
                anim.SetTrigger("play_fechar");
                Debug.Log("fechando a mão...");
                break;
            case "abre":
                anim.SetTrigger("play_abrir");
                Debug.Log("Abrindo a mão...");
                break;
            case "flexao":
                anim.SetTrigger("play_flexao");
                Debug.Log("Realizando flexão da mão...");
                break;

            case "extensao":
                anim.SetTrigger("play_extensao");
                Debug.Log("Realizando extensão da mão...");
                break;

            case "supinacao":
                anim.SetTrigger("play_supinacao");
                Debug.Log("Realizando supinação da mão...");
                break;

            case "pronacao":
                anim.SetTrigger("play_pronacao");
                Debug.Log("Realizando pronação da mão...");
                break;
        }

        msg = "";


        if (Input.GetKey("down"))
        {
            //reset_all_other_triggers("play_fechar");
            anim.SetTrigger("play_fechar");
            Debug.Log("Fechando a mão...");
        }
        else if (Input.GetKey("up"))
        {
            // reset_all_other_triggers("play_abrir");
            anim.SetTrigger("play_abrir");
            Debug.Log("Abrindo a mão...");
        }
        else if (Input.GetKey("left"))
        {
            // reset_all_other_triggers("play_flexao");
            anim.SetTrigger("play_flexao");
            Debug.Log("Realizando flexão da mão...");

        }
        else if (Input.GetKey("right"))
        {
            //reset_all_other_triggers("play_flexao");
            anim.SetTrigger("play_extensao");
            Debug.Log("Realizando extensão da mão...");

        }
        else if (Input.GetKey("s"))
        {
            //reset_all_other_triggers("play_supinacao");
            anim.SetTrigger("play_supinacao");
            Debug.Log("Realizando supinação da mão...");

        }
        else if (Input.GetKey("p"))
        {
            //reset_all_other_triggers("play_pronacao");
            anim.SetTrigger("play_pronacao");
            Debug.Log("Realizando pronação da mão...");
        }
    }

    //void reset_all_other_triggers(String except_trigger)
    //{
    //    triggers.Remove(except_trigger);
    //    triggers.ForEach(trigger_to_remove => anim.ResetTrigger(trigger_to_remove));
    //    triggers.Add(except_trigger);

    //}
}

